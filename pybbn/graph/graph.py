class Graph:
    def __init__(self):
        self.nodes = dict()
        self.edges = dict()
        self.map = dict()

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_edge(self, edge):
        self.add_node(edge.i)
        self.add_node(edge.j)
        self.edges[edge.key] = edge

        if edge.i.id not in self.map:
            self.map[edge.i.id] = set()
        if edge.j.id not in self.map:
            self.map[edge.j.id] = set()

        self.map[edge.i.id].add(edge.j.id)
        self.map[edge.j.id].add(edge.i.id)

    def get_nodes(self):
        return self.nodes.values()

    def get_edges(self):
        return self.edges.values()

    def get_neighbors(self, id):
        return map(lambda k: self.nodes[k], self.map[id])
