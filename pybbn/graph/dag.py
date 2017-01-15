from pybbn.graph.graph import Graph
from pybbn.graph.node import BbnNode
from pybbn.graph.edge import EdgeType


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

