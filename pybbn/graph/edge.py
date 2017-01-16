from enum import Enum


class EdgeType(Enum):
    UNDIRECTED = 1
    DIRECTED = 2


class Edge:
    def __init__(self, i, j, type):
        self.i = i
        self.j = j
        self.type = type

    @property
    def key(self):
        a = min(self.i.id, self.j.id)
        b = max(self.i.id, self.j.id)

        edge = '--'
        if EdgeType.DIRECTED == self.type:
            edge = '->'

        return "{}{}{}".format(a, edge, b)

    def __str__(self):
        return self.key


class SepSetEdge(Edge):
    def __init__(self, i, j):
        Edge.__init__(self, i, j, EdgeType.UNDIRECTED)

    def __str__(self):
        a = min(self.i.id, self.j.id)
        b = max(self.i.id, self.j.id)

        lhs = self.i.__str__() if a == self.i.id else self.j.__str__()
        rhs = self.j.__str__() if b == self.j.id else self.i.__str__()

        edge = '--'

        return "{}{}{}".format(lhs, edge, rhs)


class JtEdge(Edge):
    def __init__(self, sep_set):
        Edge.__init__(self, sep_set.left, sep_set.right, EdgeType.UNDIRECTED)
        self.sep_set = sep_set

    def get_lhs_edge(self):
        return SepSetEdge(self.sep_set.left, self.sep_set)

    def get_rhs_edge(self):
        return SepSetEdge(self.sep_set.right, self.sep_set)

    def __str__(self):
        return '{}--{}--{}'.format(self.sep_set.left.__str__(), self.sep_set.__str__(), self.sep_set.right.__str__())

