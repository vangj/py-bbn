from pybbn.graph.graph import Graph
from pybbn.graph.node import BbnNode
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.variable import Variable


class Dag(Graph):
    def __init__(self):
        Graph.__init__(self)

    def get_parents(self, id):
        return [x for x in self.map if id in self.map[x]]

    def get_children(self, id):
        return [x for x in self.map[id]]

    def __shouldadd__(self, edge):
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
        if id2 in self.map[id1]:
            return True
        return False


class Bbn(Dag):
    def __init__(self):
        Dag.__init__()

    def __shouldadd__(self, edge):
        if isinstance(edge.i, BbnNode) and isinstance(edge.j, BbnNode):
            return True
        return Dag.__shouldadd__(edge)


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
        children = self.graph.get_children(i)
        if self.stop in children:
            return True

        self.seen.add(i)
        for child in children:
            if child not in self.seen and self.find(child):
                return True

        return False


class BbnUtil:
    @staticmethod
    def get_huang_graph():
        a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
        b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
        c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])
        d = BbnNode(Variable(3, 'd', ['on', 'off']), [0.9, 0.1, 0.5, 0.5])
        e = BbnNode(Variable(4, 'e', ['on', 'off']), [0.3, 0.7, 0.6, 0.4])
        f = BbnNode(Variable(5, 'f', ['on', 'off']), [0.01, 0.99, 0.01, 0.99, 0.01, 0.99, 0.99, 0.01])
        g = BbnNode(Variable(6, 'g', ['on', 'off']), [0.8, 0.2, 0.1, 0.9])
        h = BbnNode(Variable(7, 'h', ['on', 'off']), [0.05, 0.95, 0.95, 0.05, 0.95, 0.05, 0.95, 0.05])

        bbn = Bbn()\
            .add_node(a)\
            .add_node(b)\
            .add_node(c)\
            .add_node(d)\
            .add_node(e)\
            .add_node(f)\
            .add_node(g)\
            .add_node(h)\
            .add_edge(Edge(a, b, EdgeType.DIRECTED))\
            .add_edge(Edge(a, c, EdgeType.DIRECTED))\
            .add_edge(Edge(b, d, EdgeType.DIRECTED))\
            .add_edge(Edge(c, e, EdgeType.DIRECTED))\
            .add_edge(Edge(d, f, EdgeType.DIRECTED))\
            .add_edge(Edge(e, f, EdgeType.DIRECTED))\
            .add_edge(Edge(c, g, EdgeType.DIRECTED))\
            .add_edge(Edge(e, h, EdgeType.DIRECTED))\
            .add_edge(Edge(g, h, EdgeType.DIRECTED))

        return bbn