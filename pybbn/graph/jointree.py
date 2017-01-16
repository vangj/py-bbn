from pybbn.graph.graph import Ug
from pybbn.graph.potential import Potential, PotentialEntry, PotentialUtil
from pybbn.graph.node import Clique, SepSet
from pybbn.graph.edge import JtEdge
from enum import Enum


class JoinTree(Ug):
    def __init__(self):
        Ug.__init__(self)
        self.potentials = dict()
        self.evidences = dict()
        self.listener = None

    def get_bbn_potential(self, node):
        clique = node.metadata['parent.clique']
        return PotentialUtil.normalize(PotentialUtil.marginalize_for(self, clique, [node]))

    def unmark_cliques(self):
        for clique in self.get_cliques():
            clique.unmark()

    def get_bbn_nodes(self):
        nodes = dict()
        for clique in self.get_cliques():
            for node in clique.nodes:
                nodes[node.id] = node
        return list(nodes.values())

    def get_bbn_node(self, id):
        for node in self.get_bbn_node():
            if id == node.id:
                return node
        return None

    def get_bbn_node_by_name(self, name):
        for node in self.get_bbn_node():
            if name == node.variable.name:
                return node
        return None

    def find_cliques_with_node_and_parents(self, id):
        ids = self.__get_parent_ids__(id)
        ids.append(id)

        set1 = set(ids)
        return [clique for clique in self.get_cliques() if set(clique.get_node_ids()).issuperset(set1)]

    def add_potential(self, clique, potential):
        self.potentials[clique.id] = potential
        return self

    def get_cliques(self):
        return [clique for clique in self.get_nodes() if isinstance(clique, Clique)]

    def get_sep_sets(self):
        return [sep_set for sep_set in self.get_nodes() if isinstance(sep_set, SepSet)]

    def add_edge(self, edge):
        if not isinstance(edge, JtEdge):
            return self
        if self.__shouldadd__(edge):
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

            self.map[lhs.id].add(sep_set.id)
            self.map[rhs.id].add(sep_set.id)

            self.map[sep_set.id].add(lhs.id)
            self.map[sep_set.id].add(rhs.id)

        return self

    def set_listener(self, listener):
        self.listener = listener

    def get_evidence(self, node, value):
        if node.id not in self.evidences:
            self.evidences[node.id] = dict()

        if value not in self.evidences[node.id]:
            entry = PotentialEntry()
            entry.add(node.id, value)
            entry.value = 1.0

            potential = Potential()
            potential.add_entry(entry)

            self.evidences[node.id] = potential

        return self.evidences[node.id][value]

    def get_change_type(self, evidences):
        changes = []
        for evidence in evidences:
            node = evidence.node
            clique = self.find_cliques_with_node_and_parents(node.id)[0]
            potentials = self.evidences[node.id]
            change = evidence.compare(potentials)
            changes.append(change)

        count = len([change for change in changes if ChangeType.RETRACTION == change])
        if count > 0:
            return ChangeType.RETRACTION

        count = len([change for change in changes if ChangeType.UPDATE == change])
        if count > 0:
            return ChangeType.UPDATE

        return ChangeType.NONE

    def get_unobserved_evidence(self, node):
        evidence = Evidence(node, EvidenceType.UNOBSERVE)
        for value in node.variable.values:
            evidence.add_value(value, 1.0)
        return evidence

    def unobserve(self, nodes):
        evidences = [self.get_unobserved_evidence(node) for node in nodes]
        self.update_evidences(evidences)
        return self

    def unobserve_all(self):
        self.unobserve(self.get_bbn_nodes())
        return self

    def update_evidences(self, evidences):
        for evidence in evidences:
            evidence.validate()
        change = self.get_change_type(evidences)
        for evidence in evidences:
            node = evidence.node
            potentials = self.evidences[node.id]

            for k, v in evidence.values:
                potential = potentials[k]
                potential.entries[0].value = v
        self.__notify_listener__(change)
        return self

    def set_observation(self, evidence):
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
        lhs = edge.i
        rhs = edge.j

        if lhs.id == rhs.id:
            return False

        if not PathDetector(self, lhs.id, rhs.id).exists():
            return True

        return False

    def __get_parent_ids__(self, id):
        node = self.get_bbn_node(id)
        if 'parents' in node.metadata:
            return [node.id for node in node.metadata['parents']]
        return []

    def __notify_listener__(self, change):
        if self.listener is None:
            return
        if ChangeType.RETRACTION == change:
            self.listener.evidence_retracted(self)
        elif ChangeType.UPDATE == change:
            self.listener.evidence_updated(self)


class PathDetector:
    def __init__(self, graph, start, stop):
        self.graph = graph
        self.start = start
        self.stop = stop
        self.seen = set()

    def exists(self):
        if self.start == self.stop:
            return True
        else:
            return self.find(self.start)

    def find(self, i):
        neighbors = self.graph.get_neighbors(i)
        if self.stop in neighbors:
            return True

        self.seen.add(i)
        for neighbor in neighbors:
            if neighbor not in self.seen and self.find(neighbor):
                return True

        return False


class JoinTreeListener(object):
    def evidence_retracted(self, join_tree):
        pass

    def evidence_updated(self, join_tree):
        pass


class EvidenceType(Enum):
    VIRTUAL = 1
    FINDING = 2
    OBSERVATION = 3
    UNOBSERVE = 4


class ChangeType(Enum):
    NONE = 1
    UPDATE = 2
    RETRACTION = 3


class EvidenceBuilder:
    def __init__(self):
        self.values = dict()
        self.node = None
        self.type = EvidenceType.OBSERVATION

    def with_node(self, node):
        self.node = node
        return self

    def with_type(self, type):
        self.type = type
        return self

    def with_evidence(self, val, likelihood):
        self.values[val] = likelihood
        return self

    def build(self):
        evidence = Evidence(self.node, self.type)
        for k, v in self.values:
            evidence.add_value(k, v)
        return evidence


class Evidence:
    def __init__(self, node, type):
        self.node = node
        self.type = type
        self.values = dict()

    def add_value(self, value, likelihood):
        self.values[value] = likelihood
        return self

    def compare(self, potentials):
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
        m = dict()
        for k, v in potentials:
            m[k] = v.entries[0].value
        return m

    @staticmethod
    def __is_unobserved__(values):
        count = 0
        for k, v in values:
            count += v
        return count == len(values)

    @staticmethod
    def __is_observed__(values):
        one = 0
        zero = 0

        for k, v in values:
            if 1.0 == v:
                one += 1
            else:
                zero += 1

        return 1 == one and len(values) - 1 == zero

    @staticmethod
    def __get_observed_value__(values):
        strs = [k for k in values if 1.0 == values[k]]
        return strs[0]

    def validate(self):
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
            key = [k for k in self.values.keys()].sort(None, lambda k: self.values[k], True)[0]
            for value in self.node.variable.values:
                if key == value:
                    self.values[value] = 1.0
                else:
                    self.values[value] = 0.0
        elif EvidenceType.UNOBSERVE == self.type:
            for value in self.node.variable.values:
                self.values[value] = 1.0

