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
    def __init__(self, sepSet):
        Edge.__init__(sepSet.left, sepSet.right, EdgeType.UNDIRECTED)
        self.sepSet = sepSet

    def __str__(self):
        return '{}--{}--{}'.format(self.sepSet.left.__str__(), self.sepSet.__str__(), self.sepSet.right.__str__())

