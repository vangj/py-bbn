class ShortestPath:
    def __init__(self, start, stop, graph):
        self.start = start
        self.stop = stop
        self.graph = graph
        self.seen = set()

    def exists(self):
        if self.start == self.stop:
            return True
        else:
            return self.search(self.start)

    def search(self, i):
        self.seen.add(i)
        for node_id in self.graph.get_neighbors(i):
            if node_id == self.stop:
                return True
            if node_id not in self.seen:
                if self.search(node_id):
                    return True
        return False
