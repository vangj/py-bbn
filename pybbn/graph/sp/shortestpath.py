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
        for n in self.graph.get_neighbors(i):
            if n.uid == self.stop:
                return True
            if n.uid not in self.seen:
                if self.search(n.uid):
                    return True
        return False
