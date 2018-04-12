from enum import Enum

from pybbn.graph.edge import JtEdge
from pybbn.graph.graph import Ug
from pybbn.graph.node import SepSet
from pybbn.graph.potential import Potential, PotentialEntry, PotentialUtil


class JoinTree(Ug):
    """
    Join tree.
    """

    def __init__(self):
        """
        Ctor.
        """
        Ug.__init__(self)
        self.potentials = dict()
        self.evidences = dict()
        self.listener = None

    def get_bbn_potential(self, node):
        """
        Gets the potential associated with the specified BBN node.
        :param node: BBN node.
        :return: Potential.
        """
        clique = node.metadata['parent.clique']
        return PotentialUtil.normalize(PotentialUtil.marginalize_for(self, clique, [node]))

    def unmark_cliques(self):
        """
        Unmarks the cliques.
        """
        for clique in self.get_cliques():
            clique.unmark()

    def get_bbn_nodes(self):
        """
        Gets all the BBN nodes in this junction tree.
        :return: List of BBN nodes.
        """
        nodes = dict()
        for clique in self.get_cliques():
            for node in clique.nodes:
                nodes[node.id] = node
        return list(nodes.values())

    def get_bbn_node(self, id):
        """
        Gets the BBN node associated with the specified id.
        :param id: Node id.
        :return: BBN node or None if no such node exists.
        """
        for node in self.get_bbn_nodes():
            if id == node.id:
                return node
        return None

    def get_bbn_node_by_name(self, name):
        """
        Gets the BBN node associated with the specified name.
        :param name: Node name.
        :return: BBN node or None if no such node exists.
        """
        for node in self.get_bbn_nodes():
            if name == node.variable.name:
                return node
        return None

    def find_cliques_with_node_and_parents(self, id):
        """
        Finds all cliques in this junction tree having the specified node and its parents.
        :param id: Node id.
        :return: Array of cliques.
        """
        ids = self.__get_parent_ids__(id)
        ids.append(id)

        set1 = set(ids)
        return [clique for clique in self.get_cliques() if set(clique.get_node_ids()).issuperset(set1)]

    def add_potential(self, clique, potential):
        """
        Adds a potential associated with the specified clique.
        :param clique: Clique.
        :param potential: Potential.
        :return: This join tree.
        """
        self.potentials[clique.id] = potential
        return self

    def get_cliques(self):
        """
        Gets all the cliques in this junction tree.
        :return: Array of cliques.
        """
        return [clique for clique in self.get_nodes() if not isinstance(clique, SepSet)]

    def get_sep_sets(self):
        """
        Gets all the separation sets in this junction tree.
        :return: Array of separation sets.
        """
        return [sep_set for sep_set in self.get_nodes() if isinstance(sep_set, SepSet)]

    def add_edge(self, edge):
        """
        Adds an JtEdge.
        :param edge: JtEdge.
        :return: This join tree.
        """
        if not isinstance(edge, JtEdge):
            return self

        sep_set = edge.sep_set
        lhs = edge.i
        rhs = edge.j

        self.add_node(sep_set)
        self.add_node(lhs)
        self.add_node(rhs)

        if sep_set.id not in self.map:
            self.map[sep_set.id] = set()
        if lhs.id not in self.map:
            self.map[lhs.id] = set()
        if rhs.id not in self.map:
            self.map[rhs.id] = set()

        if self.__shouldadd__(edge):
            self.map[lhs.id].add(sep_set.id)
            self.map[rhs.id].add(sep_set.id)

            self.map[sep_set.id].add(lhs.id)
            self.map[sep_set.id].add(rhs.id)

            self.edges[edge.key] = edge
            # lhs_edge = edge.get_lhs_edge()
            # rhs_edge = edge.get_rhs_edge()
            # self.edges[lhs_edge.key] = lhs_edge
            # self.edges[rhs_edge.key] = rhs_edge

        return self

    def get_flattened_edges(self):
        """
        Gets all the edges "flattened" out. Since separation-sets are really hyper-edges, this method breaks
        separation-sets into two edges.
        :return: Array of edges.
        """
        edges = []
        for edge in self.edges.values():
            edges.append(edge.get_lhs_edge())
            edges.append(edge.get_rhs_edge())
        return edges

    def set_listener(self, listener):
        """
        Sets the listener.
        :param listener: JoinTreeListener.
        """
        self.listener = listener

    def get_evidence(self, node, value):
        """
        Gets the evidence associated with the specified BBN node and value.
        :param node: BBN node.
        :param value: Value.
        :return: Potential (the evidence).
        """
        if node.id not in self.evidences:
            self.evidences[node.id] = dict()

        if value not in self.evidences[node.id]:
            entry = PotentialEntry()
            entry.add(node.id, value)
            entry.value = 1.0

            potential = Potential()
            potential.add_entry(entry)

            self.evidences[node.id][value] = potential

        return self.evidences[node.id][value]

    def get_change_type(self, evidences):
        """
        Gets the change type associated with the specified list of evidences.
        :param evidences: List of evidences.
        :return: ChangeType.
        """
        changes = []
        for evidence in evidences:
            node = evidence.node
            potentials = self.evidences[node.id]
            change = evidence.compare(potentials)
            changes.append(change)

        count = len([change_type for change_type in changes if ChangeType.RETRACTION == change_type])
        if count > 0:
            return ChangeType.RETRACTION

        count = len([change_type for change_type in changes if ChangeType.UPDATE == change_type])
        if count > 0:
            return ChangeType.UPDATE

        return ChangeType.NONE

    def get_unobserved_evidence(self, node):
        """
        Gets the unobserved evidences associated with the specified node.
        :param node: BBN node.
        :return: Evidence.
        """
        evidence = Evidence(node, EvidenceType.UNOBSERVE)
        for value in node.variable.values:
            evidence.add_value(value, 1.0)
        return evidence

    def unobserve(self, nodes):
        """
        Unobserves a list of nodeds.
        :param nodes: List of nodes.
        :return: This join tree.
        """
        evidences = [self.get_unobserved_evidence(node) for node in nodes]
        self.update_evidences(evidences)
        return self

    def unobserve_all(self):
        """
        Unobserves all BBN nodes.
        :return: This join tree.
        """
        self.unobserve(self.get_bbn_nodes())
        return self

    def update_evidences(self, evidences):
        """
        Updates this join tree with the list of specified evidence.
        :param evidences: List of evidences.
        :return: This join tree.
        """
        for evidence in evidences:
            evidence.validate()
        change = self.get_change_type(evidences)
        for evidence in evidences:
            node = evidence.node
            potentials = self.evidences[node.id]

            for k, v in evidence.values.items():
                potential = potentials[k]
                potential.entries[0].value = v
        self.__notify_listener__(change)
        return self

    def set_observation(self, evidence):
        """
        Sets a single observation.
        :param evidence: Evidence.
        :return: This join tree.
        """
        if EvidenceType.OBSERVATION != evidence.type:
            return self

        potentials = self.evidences[evidence.node.id]

        pvalues = []
        for v, potential in potentials.items():
            entry = potential.entries[0]
            p = entry.value
            if 1.0 == p:
                pvalues.append(v)

        cvalues = []
        for v, likelihood in evidence.values.items():
            if 1.0 == likelihood:
                cvalues.append(v)

        if 1 == len(pvalues):
            last_value = pvalues[0]
            curr_value = cvalues[0]
            if last_value == curr_value:
                self.unobserve([evidence.node])
            else:
                self.update_evidences([evidence])
        else:
            self.update_evidences([evidence])

        return self

    def __shouldadd__(self, edge):
        """
        Checks if the specified edge should be added.
        :param edge: Edge.
        :return: A boolean indicating if the specified edge should be added.
        """
        lhs = edge.i
        rhs = edge.j

        if lhs.id == rhs.id:
            return False

        if not PathDetector(self, lhs.id, rhs.id).exists():
            return True

        return False

    def __get_parent_ids__(self, id):
        """
        Gets the parent ids of the specified node id.
        :param id: Node id.
        :return: Array of parent ids.
        """
        node = self.get_bbn_node(id)
        if 'parents' in node.metadata:
            return [n.id for n in node.metadata['parents']]
        return []

    def __notify_listener__(self, change):
        """
        Notifies the JoinTreeListener, if any.
        :param change: ChangeType.
        """
        if self.listener is None:
            return
        if ChangeType.RETRACTION == change:
            self.listener.evidence_retracted(self)
        elif ChangeType.UPDATE == change:
            self.listener.evidence_updated(self)


class PathDetector(object):
    """
    Detects path between two nodes.
    """

    def __init__(self, graph, start, stop):
        """
        Ctor.
        :param graph: Join tree.
        :param start: Start node id.
        :param stop: Stop node id.
        """
        self.graph = graph
        self.start = start
        self.stop = stop
        self.seen = set()

    def exists(self):
        """
        Checks if a path exists.
        :return: True if a path exists, otherwise, false.
        """
        if self.start == self.stop:
            return True
        else:
            return self.__find__(self.start)

    def __find__(self, i):
        """
        Checks if a path exists from the specified node to the stop node.
        :param i: Node id.
        :return: True if a path exists, otherwise, false.
        """
        neighbors = self.graph.get_neighbors(i)
        if self.stop in neighbors:
            return True

        self.seen.add(i)
        for neighbor in neighbors:
            if neighbor not in self.seen and self.__find__(neighbor):
                return True

        return False


class JoinTreeListener(object):
    """
    Interface like class used for listening to a join tree.
    """

    def evidence_retracted(self, join_tree):
        """
        Evidence is retracted.
        :param join_tree: Join tree.
        """
        pass

    def evidence_updated(self, join_tree):
        """
        Evidence is updated.
        :param join_tree: Join tree.
        """
        pass


class EvidenceType(Enum):
    """
    Evidence type.
    """
    VIRTUAL = 1
    FINDING = 2
    OBSERVATION = 3
    UNOBSERVE = 4


class ChangeType(Enum):
    """
    Change type.
    """
    NONE = 1
    UPDATE = 2
    RETRACTION = 3


class EvidenceBuilder(object):
    """
    Evidence builder.
    """

    def __init__(self):
        """
        Ctor.
        """
        self.values = dict()
        self.node = None
        self.type = EvidenceType.OBSERVATION

    def with_node(self, node):
        """
        Adds a BBN node.
        :param node: BBN node.
        :return: Builder.
        """
        self.node = node
        return self

    def with_type(self, type):
        """
        Adds the EvidenceType.
        :param type: EvidenceType.
        :return: Builder.
        """
        self.type = type
        return self

    def with_evidence(self, val, likelihood):
        """
        Adds evidence.
        :param val: Value.
        :param likelihood: Likelihood.
        :return: Builder.
        """
        self.values[val] = likelihood
        return self

    def build(self):
        """
        Builds an evidence.
        :return: Evidence.
        """
        evidence = Evidence(self.node, self.type)
        for k, v in self.values.items():
            evidence.add_value(k, v)
        return evidence


class Evidence(object):
    """
    Evidence.
    """

    def __init__(self, node, type):
        """
        Ctor.
        :param node: BBN node.
        :param type: EvidenceType.
        """
        self.node = node
        self.type = type
        self.values = dict()

    def add_value(self, value, likelihood):
        """
        Adds a value.
        :param value: Value.
        :param likelihood: Likelihood.
        :return: This evidence.
        """
        self.values[value] = likelihood
        return self

    def compare(self, potentials):
        """
        Compares this evidence with previous ones.
        :param potentials: Map of potentials.
        :return: The ChangeType from the comparison.
        """
        that = self.__convert__(potentials)

        that_unobserve = self.__is_unobserved__(that)
        this_unobserve = self.__is_unobserved__(self.values)

        if that_unobserve and this_unobserve:
            return ChangeType.NONE

        that_observe = self.__is_observed__(that)
        this_observe = self.__is_observed__(self.values)

        if that_observe and this_observe:
            s1 = self.__get_observed_value__(that)
            s2 = self.__get_observed_value__(self.values)

            if s1 == s2:
                return ChangeType.NONE
            else:
                return ChangeType.RETRACTION

        return ChangeType.RETRACTION

    @staticmethod
    def __convert__(potentials):
        """
        Converts potentials to a map (dict).
        :param potentials: Potentials.
        :return: Dict where keys are BBN node values and values are likelihoods.
        """
        m = dict()
        for k, v in potentials.items():
            m[k] = v.entries[0].value
        return m

    @staticmethod
    def __is_unobserved__(values):
        """
        Checks if the values represent an unobserved evidence. If all likelihoods are 1.0, then this
        map of values represent unobserved evidence.
        :param values: Map of values, where keys are values and values are likelihoods.
        :return: A boolean indicating if the values represent unobserved evidence.
        """
        count = 0
        for k, v in values.items():
            count += v
        return count == len(values)

    @staticmethod
    def __is_observed__(values):
        """
        Checks if the values represent an observed evidence. If all likelihoods are 0 with exactly
        one of them being 1, then this map of values represent observed evidence.
        :param values: Map of values, where keys are values and values are likelihoods.
        :return: A boolean indicating if the values represent observed evidence.
        """
        one = 0
        zero = 0

        for k, v in values.items():
            if 1.0 == v:
                one += 1
            else:
                zero += 1

        return 1 == one and len(values) - 1 == zero

    @staticmethod
    def __get_observed_value__(values):
        """
        Gets the value that is observed (the value whose likelihood is 1.0).
        :param values: Map of values, where keys are values and values are likelihoods.
        :return: Observed value.
        """
        strs = [k for k in values if 1.0 == values[k]]
        return strs[0]

    def validate(self):
        """
        Validates this evidence.

        * virtual evidence: sum of likelihoods must equal to 1.0
        * finding evidence: all likelihoods must be exactly 1.0 or 0.0.
        * observation evidence: exactly one likelihood is 1.0 and all others must be 0.0.
        """
        for value in self.node.variable.values:
            if value not in self.values:
                self.values[value] = 0.0

        if EvidenceType.VIRTUAL == self.type:
            total = sum([x for x in self.values.values()])
            for value in self.node.variable.values:
                d = self.values[value] / total
                self.values[value] = d
        elif EvidenceType.FINDING == self.type:
            for value in self.node.variable.values:
                d = 1.0 if self.values[value] > 0.0 else 0.0
                self.values[value] = d

            count = sum([x for x in self.values.values()])
            if 0.0 == count:
                for value in self.node.variable.values:
                    self.values[value] = 1.0
        elif EvidenceType.OBSERVATION == self.type:
            tuples = []
            for k, v in self.values.items():
                pair = (k, v)
                tuples.append(pair)
            tuples = sorted(tuples, key=lambda x: (x[1]), reverse=True)
            key = tuples[0][0]
            for value in self.node.variable.values:
                if key == value:
                    self.values[value] = 1.0
                else:
                    self.values[value] = 0.0
        elif EvidenceType.UNOBSERVE == self.type:
            for value in self.node.variable.values:
                self.values[value] = 1.0
