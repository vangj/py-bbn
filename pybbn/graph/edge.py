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


class JtEdge(Edge):
    def __init__(self, sep_set):
        Edge.__init__(sep_set.left, sep_set.right, EdgeType.UNDIRECTED)
        self.sep_set = sep_set

    def __str__(self):
        return '{}--{}--{}'.format(self.sep_set.left.__str__(), self.sep_set.__str__(), self.sep_set.right.__str__())

