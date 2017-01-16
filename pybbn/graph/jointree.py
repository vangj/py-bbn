from pybbn.graph.graph import Ug
from enum import Enum


class JoinTree(Ug):
    def __init__(self):
        Ug.__init__(self)
        self.potentials = dict()
        self.evidences = dict()
        self.listener = None

    def get_bbn_potential(self, node):
        clique = node.metadata['parent.clique']
        return None

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

