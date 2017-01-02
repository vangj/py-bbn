class Graph:
    def __init__(self):
        self.nodes = dict()
        self.edges = dict()
        self.map = dict()

    def add_node(self, node):
        self.nodes[node.key] = node

    def add_edge(self, edge):
        self.add_node(edge.i)
        self.add_node(edge.j)
        self.edges[edge.key] = edge

        if edge.i.uid not in self.map:
            self.map[edge.i.uid] = set()
        if edge.j.uid not in self.map:
            self.map[edge.j.uid] = set()

        self.map[edge.i.uid].add(edge.j.uid)
        self.map[edge.j.uid].add(edge.i.uid)

    def get_nodes(self):
        return self.nodes.values()

    def get_edges(self):
        return self.edges.values()

    def get_neighbors(self, uid):
        return map(lambda k: self.nodes[k], self.map[uid])
