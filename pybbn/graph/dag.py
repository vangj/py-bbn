from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.graph import Graph
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable


class Dag(Graph):
    """
    Directed acyclic graph.
    """

    def __init__(self):
        """
        Ctor.
        """
        Graph.__init__(self)

    def get_parents(self, id):
        """
        Gets the parent IDs of the specified node.
        :param id: Node id.
        :return: Array of parent ids.
        """
        return [x for x in self.map if id in self.map[x]]

    def get_children(self, node_id):
        """
        Gets the children IDs of the specified node.
        :param node_id: Node id.
        :return: Array of children ids.
        """
        return [x for x in self.map[node_id]]

    def __shouldadd__(self, edge):
        """
        Checks if the specified directed edge should be added.
        :param edge: Directed edge.
        :return: A boolean indicating if the edge should be added.
        """
        if EdgeType.DIRECTED != edge.type:
            return False

        parent = edge.i
        child = edge.j

        if parent.id == child.id:
            return False

        if child.id not in self.map[parent.id] and parent.id not in self.map[child.id]:
            if not PathDetector(self, child.id, parent.id).exists():
                return True

        return False

    def edge_exists(self, id1, id2):
        """
        Checks if a directed edge exists between the specified id. e.g. id1 -> id2
        :param id1: Node id.
        :param id2: Node id.
        :return: A boolean indicating if a directed edge id1 -> id2 exists.
        """
        if id2 in self.map[id1] and id1 not in self.map[id2]:
            return True
        return False


class Bbn(Dag):
    """
    BBN.
    """

    def __init__(self):
        """Ctor."""
        Dag.__init__(self)
        self.parents = {}

    def get_parents_ordered(self, id):
        return self.parents[id] if id in self.parents else []

    def __edge_added__(self, edge):
        if edge.j.id not in self.parents:
            self.parents[edge.j.id] = []

        if edge.i.id not in self.parents[edge.j.id]:
            self.parents[edge.j.id].append(edge.i.id)

    def __shouldadd__(self, edge):
        """
        Checks if the specified directed edge should be added.
        :param edge: Directed edge.
        :return: A boolean indicating if the directed edge should be added.
        """
        if isinstance(edge.i, BbnNode) and isinstance(edge.j, BbnNode):
            return True
        return Dag.__shouldadd__(edge)


class PathDetector(object):
    """
    Detects path between two nodes.
    """

    def __init__(self, graph, start, stop):
        """
        :param graph: DAG.
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
        children = self.graph.get_children(i)
        if self.stop in children:
            return True

        self.seen.add(i)
        for child in children:
            if child not in self.seen and self.__find__(child):
                return True

        return False


class BbnUtil(object):
    """
    BBN utility.
    """

    @staticmethod
    def get_huang_graph():
        """
        Gets the Huang reference BBN graph.
        :return: BBN.
        """
        a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
        b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
        c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])
        d = BbnNode(Variable(3, 'd', ['on', 'off']), [0.9, 0.1, 0.5, 0.5])
        e = BbnNode(Variable(4, 'e', ['on', 'off']), [0.3, 0.7, 0.6, 0.4])
        f = BbnNode(Variable(5, 'f', ['on', 'off']), [0.01, 0.99, 0.01, 0.99, 0.01, 0.99, 0.99, 0.01])
        g = BbnNode(Variable(6, 'g', ['on', 'off']), [0.8, 0.2, 0.1, 0.9])
        h = BbnNode(Variable(7, 'h', ['on', 'off']), [0.05, 0.95, 0.95, 0.05, 0.95, 0.05, 0.95, 0.05])

        bbn = Bbn() \
            .add_node(a) \
            .add_node(b) \
            .add_node(c) \
            .add_node(d) \
            .add_node(e) \
            .add_node(f) \
            .add_node(g) \
            .add_node(h) \
            .add_edge(Edge(a, b, EdgeType.DIRECTED)) \
            .add_edge(Edge(a, c, EdgeType.DIRECTED)) \
            .add_edge(Edge(b, d, EdgeType.DIRECTED)) \
            .add_edge(Edge(c, e, EdgeType.DIRECTED)) \
            .add_edge(Edge(d, f, EdgeType.DIRECTED)) \
            .add_edge(Edge(e, f, EdgeType.DIRECTED)) \
            .add_edge(Edge(c, g, EdgeType.DIRECTED)) \
            .add_edge(Edge(e, h, EdgeType.DIRECTED)) \
            .add_edge(Edge(g, h, EdgeType.DIRECTED))

        return bbn
