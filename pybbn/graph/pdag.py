from pybbn.graph.graph import Graph


class Pdag(Graph):
    def __init__(self):
        Graph.__init__(self)

    def get_parents(self, id):
        return [x for x in self.map if id in self.map[x]]

    def get_out_nodes(self, id):
        parents = self.get_parents(id)
        neighbors = self.get_neighbors(id)
        out_nodes = [id for id in neighbors if id not in parents]
        return out_nodes

    def __shouldadd__(self, edge):
        parent = edge.i
        child = edge.j

        if parent.id == child.id:
            return False

        if child.id not in self.map[parent.id] and parent.id not in self.map[child.id]:
            if not PathDetector(self, child.id, parent.id).exists():
                return True

        return False

    def edge_exists(self, id1, id2):
        if id2 in self.map[id1] or id1 in self.map[id2]:
            return True
        return False

    def directed_edge_exists(self, id1, id2):
        if id2 in self.map[id1] and id1 not in self.map[id2]:
            return True
        return False


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
        out_nodes = self.graph.get_out_nodes(i)
        if self.stop in out_nodes:
            return True

        self.seen.add(i)
        for out_node in out_nodes:
            if out_node not in self.seen and self.find(out_node):
                return True

        return False
