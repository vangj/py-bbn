from collections import defaultdict
from copy import deepcopy
from enum import Enum

from pybbn.graph.edge import JtEdge
from pybbn.graph.graph import Ug
from pybbn.graph.node import SepSet, Clique, BbnNode
from pybbn.graph.potential import Potential, PotentialEntry, PotentialUtil
from pybbn.graph.variable import Variable


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
        self.parent_info = defaultdict(set)
        # self.__all_nodes__ = None

    def __deepcopy__(self, memodict={}):
        nodes = deepcopy(self.nodes, memodict)
        edges = deepcopy(self.edges, memodict)
        edge_map = deepcopy(self.edge_map, memodict)
        neighbors = deepcopy(self.neighbors, memodict)
        potentials = deepcopy(self.potentials, memodict)
        evidences = deepcopy(self.evidences, memodict)
        parent_info = deepcopy(self.parent_info, memodict)

        jt = JoinTree()
        jt.nodes = nodes
        jt.edges = edges
        jt.edge_map = edge_map
        jt.neighbors = neighbors
        jt.potentials = potentials
        jt.evidences = evidences
        jt.parent_info = parent_info
        return jt

    def get_posteriors(self):
        """
        Gets the posterior for all nodes.

        :return: Map. Keys are node names; values are map of node values to posterior probabilities.
        """
        bbn_nodes = self.get_bbn_nodes()

        posteriors = {}

        for bbn_node in bbn_nodes:
            potential = self.get_bbn_potential(bbn_node)

            m = {}
            for potential_entry in potential.entries:
                k = ''.join([f'{x}={y}' for x, y in potential_entry.entries.items()])
                m[k] = potential_entry.value

            name = bbn_node.variable.name
            posteriors[name] = m

        return posteriors

    def get_bbn_potential(self, node):
        """
        Gets the potential associated with the specified BBN node.

        :param node: BBN node.
        :return: Potential.
        """
        clique = node.metadata['parent.clique']
        potential = PotentialUtil.normalize(PotentialUtil.marginalize_for(self, clique, [node]))
        return potential

    def unmark_cliques(self):
        """
        Unmarks the cliques.
        """
        for clique in self.get_cliques():
            clique.unmark()

    def update_bbn_cpts(self, cpts):
        """
        Updates the CPTs of the BBN nodes.

        :param cpts: Dictionary of CPTs. Keys are ids of BBN node and values are new CPTs.
        :return: None
        """
        bbn_nodes = {node.id: node for clique in self.get_cliques() for node in clique.nodes}
        for idx, cpt in cpts.items():
            if idx in bbn_nodes:
                bbn_nodes[idx].probs = cpt
                bbn_nodes[idx].potential = None

    def get_bbn_node_and_parents(self):
        """
        Gets a map of nodes and its parents.

        :return: Map. Keys are node ID and values are list of nodes.
        """
        bbn_nodes = {node.id: node for clique in self.get_cliques() for node in clique.nodes}
        result = {node: [pa for pa_id, pa in bbn_nodes.items() if pa_id in self.parent_info[node_id]]
                  for node_id, node in bbn_nodes.items()}
        return result

    def __get_bbn_nodes__(self):
        """
        Gets all BBN nodes (cached).

        :return: Dictionary of BBN nodes.
        """
        # if self.__all_nodes__ is None:
        #     self.__all_nodes__ = {node.id: node for clique in self.get_cliques() for node in clique.nodes}
        # return self.__all_nodes__
        result = {node.id: node for clique in self.get_cliques() for node in clique.nodes}
        return result

    def get_bbn_nodes(self):
        """
        Gets all the BBN nodes in this junction tree.

        :return: List of BBN nodes.
        """
        return list(self.__get_bbn_nodes__().values())

    def get_bbn_node(self, id):
        """
        Gets the BBN node associated with the specified id.

        :param id: Node id.
        :return: BBN node or None if no such node exists.
        """
        bbn_nodes = self.__get_bbn_nodes__()
        if id in bbn_nodes:
            return bbn_nodes[id]
        return None

    def get_bbn_node_by_name(self, name):
        """
        Gets the BBN node associated with the specified name.

        :param name: Node name.
        :return: BBN node or None if no such node exists.
        """
        bbn_nodes = {node.variable.name: node for clique in self.get_cliques() for node in clique.nodes}
        if name in bbn_nodes:
            return bbn_nodes[name]
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
        result = [clique for clique in self.get_cliques() if clique.get_node_ids().issuperset(set1)]
        return result

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

        if self.__shouldadd__(edge):
            self.add_node(sep_set)
            self.add_node(lhs)
            self.add_node(rhs)

            self.edge_map[lhs.id].add(sep_set.id)
            self.edge_map[rhs.id].add(sep_set.id)
            self.neighbors[lhs.id].add(sep_set.id)
            self.neighbors[rhs.id].add(sep_set.id)

            self.edge_map[sep_set.id].add(lhs.id)
            self.edge_map[sep_set.id].add(rhs.id)
            self.neighbors[sep_set.id].add(lhs.id)
            self.neighbors[sep_set.id].add(rhs.id)

            self.edges[edge.key] = edge

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

        result = self.evidences[node.id][value]
        return result

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
        Unobserves a list of nodes.

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

    @staticmethod
    def to_dict(jt):
        """
        Converts a junction tree to a serializable dictionary.

        :param jt: Junction tree.
        :return: Dictionary.
        """

        def nodes_to_dict(nodes):
            d = {}
            for n in nodes:
                if isinstance(n, SepSet):
                    d[n.id] = {
                        'left': n.left.id,
                        'right': n.right.id,
                        'type': 'sepset'
                    }
                elif isinstance(n, Clique):
                    d[n.id] = {
                        'node_ids': list(n.node_ids),
                        'type': 'clique'
                    }
            return d

        def edges_to_dict(edges):
            return [e.sep_set.id for e in edges]

        bbn_nodes = {n.id: n.to_dict() for n in jt.get_bbn_nodes()}
        jt_nodes = nodes_to_dict(jt.get_nodes())
        jt_edges = edges_to_dict(jt.get_edges())

        return {
            'bbn_nodes': bbn_nodes,
            'jt': {
                'nodes': jt_nodes,
                'edges': jt_edges,
                'parent_info': jt.parent_info
            }
        }

    @staticmethod
    def from_dict(d):
        """
        Converts a dictionary to a junction tree.

        :param d: Dictionary.
        :return: Junction tree.
        """

        def get_variable(d):
            return Variable(d['id'], d['name'], d['values'])

        def get_bbn_node(d):
            return BbnNode(get_variable(d['variable']), d['probs'])

        def get_clique(d, bbn_nodes):
            return Clique([bbn_nodes[idx] if idx in bbn_nodes else bbn_nodes[str(idx)] for idx in d['node_ids']])

        def get_sep_set(lhs_clique, rhs_clique):
            _, lhs, rhs, intersection = lhs_clique.intersects(rhs_clique)
            return SepSet(lhs_clique, rhs_clique, lhs, rhs, intersection)

        bbn_nodes = {k: get_bbn_node(n) for k, n in d['bbn_nodes'].items()}

        cliques = [get_clique(clique, bbn_nodes)
                   for k, clique in d['jt']['nodes'].items() if clique['type'] == 'clique']
        cliques = {c.id: c for c in cliques}

        sepsets = [get_sep_set(cliques[s['left']], cliques[s['right']])
                   for k, s in d['jt']['nodes'].items() if s['type'] == 'sepset']
        sepsets = {s.id: s for s in sepsets}

        edges = [JtEdge(sepsets[e]) for e in d['jt']['edges']]

        jt = JoinTree()
        if len(edges) > 0:
            for e in edges:
                jt.add_edge(e)
        else:
            jt.nodes = cliques

        jt.parent_info = {int(k): v for k, v in d['jt']['parent_info'].items()}
        return jt

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
        neighbors = set()

        try:
            neighbors = self.graph.get_neighbors(i)
        except KeyError:
            pass

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

    @staticmethod
    def __normalize_value_between_zero_one__(val):
        """
        Normalizes the specified value to the range [0.0, 1.0]. If the specified value is less than 0.0 then
        0.0 is returned; if the specified value is greater than 1.0 then 1.0 is returned.

        :param val: Value.
        :return: A value in the range [0.0, 1.0].
        """
        if 0.0 <= val <= 1.0:
            return val
        elif val < 0.0:
            return 0.0
        else:
            return 1.0

    @staticmethod
    def __normalize_value_zero_or_one__(val):
        """
        Normalizes the specified value to either 0.0 or 1.0 (and nothing else). If the specified value is anything
        greater than 0.0, then a 1.0 is returned, else a 0.0 is returned.

        :param val: Value.
        :return: 0.0 or 1.0.
        """
        if val > 0.0:
            return 1.0
        else:
            return 0.0

    def validate(self):
        """
        Validates this evidence.

        * virtual evidence: each likelihood must be in the range [0, 1].
        * finding evidence: all likelihoods must be exactly 1.0 or 0.0.
        * observation evidence: exactly one likelihood is 1.0 and all others must be 0.0.
        """
        for value in self.node.variable.values:
            if value not in self.values:
                self.values[value] = 0.0

        if EvidenceType.VIRTUAL == self.type:
            for value in self.node.variable.values:
                self.values[value] = Evidence.__normalize_value_between_zero_one__(self.values[value])
        elif EvidenceType.FINDING == self.type:
            for value in self.node.variable.values:
                self.values[value] = Evidence.__normalize_value_zero_or_one__(self.values[value])

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
