from enum import Enum


class EdgeType(Enum):
    """
    Edge type.
    """
    UNDIRECTED = 1
    DIRECTED = 2


class Edge(object):
    """
    Edge.
    """

    def __init__(self, i, j, type):
        """
        Ctor.
        :param i: Node.
        :param j: Node.
        :param type: Edge type.
        """
        self.i = i
        self.j = j
        self.type = type

    @property
    def key(self):
        """
        Key used for map.
        :return: Key.
        """
        a = min(self.i.id, self.j.id)
        b = max(self.i.id, self.j.id)

        edge = '--'
        if EdgeType.DIRECTED == self.type:
            edge = '->'

        return "{}{}{}".format(a, edge, b)

    def __str__(self):
        return self.key


class SepSetEdge(Edge):
    """
    Separation set.
    """

    def __init__(self, i, j):
        """
        Ctor.
        :param i: Node.
        :param j: Node.
        """
        Edge.__init__(self, i, j, EdgeType.UNDIRECTED)

    def __str__(self):
        a = min(self.i.id, self.j.id)
        b = max(self.i.id, self.j.id)

        lhs = self.i.__str__() if a == self.i.id else self.j.__str__()
        rhs = self.j.__str__() if b == self.j.id else self.i.__str__()

        edge = '--'

        return "{}{}{}".format(lhs, edge, rhs)


class JtEdge(Edge):
    """
    Junction tree edge. This is basically a hyper-edge.
    """

    def __init__(self, sep_set):
        """
        Ctor.
        :param sep_set: Separation set.
        """
        Edge.__init__(self, sep_set.left, sep_set.right, EdgeType.UNDIRECTED)
        self.sep_set = sep_set

    def get_lhs_edge(self):
        """
        Gets a JtEdge. e.g. left -- sep_set.
        :return: JtEdge.
        """
        return SepSetEdge(self.sep_set.left, self.sep_set)

    def get_rhs_edge(self):
        """
        Gets a JtEdge. e.g. right -- sep_set.
        :return: JtEdge.
        """
        return SepSetEdge(self.sep_set.right, self.sep_set)

    def __str__(self):
        return '{}--{}--{}'.format(self.sep_set.left.__str__(), self.sep_set.__str__(), self.sep_set.right.__str__())
