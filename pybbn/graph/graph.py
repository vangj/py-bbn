from pybbn.graph.edge import EdgeType


class Graph:
    def __init__(self):
        self.nodes = dict()
        self.edges = dict()
        self.map = dict()

    def get_neighbors(self, id):
        set1 = set([x for x in self.map[id]])
        set2 = set([x for x in self.map if id in self.map[x]])
        return set1 | set2

    def get_node(self, id):
        return self.nodes[id]

    def get_nodes(self):
        return [node for node in self.nodes.values()]

    def get_edges(self):
        return [edge for edge in self.edges.values()]

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_edge(self, edge):
        self.add_node(edge.i)
        self.add_node(edge.j)

        if edge.i.id not in self.map:
            self.map[edge.i.id] = set()
        if edge.j.id not in self.map:
            self.map[edge.j.id] = set()

        if self.__shouldadd__(edge):
            self.edges[edge.key] = edge
            self.map[edge.i.id].add(edge.j.id)
            if EdgeType.UNDIRECTED == edge.type:
                self.map[edge.j.id].add(edge.i.id)

    def __shouldadd__(self, edge):
        lhs = edge.i
        rhs = edge.j

        if lhs.id == rhs.id:
            return False

        if EdgeType.UNDIRECTED == edge.type:
            if lhs.id not in self.map[rhs.id] or rhs.id not in self.map[lhs.id]:
                return True
        else:
            if rhs.id not in self.map[lhs.id]:
                return True

        return False

    def edge_exists(self, id1, id2):
        if id2 in self.map[id1] and id1 in self.map[id2]:
            return True
        return False

    def remove_node(self, id):
        self.nodes.pop(id, None)

    def __str__(self):
        nodes = str.join('\n', [x.__str__() for x in self.nodes.values()])
        edges = str.join('\n', [x.__str__() for x in self.edges.values()])
        return nodes + '\n' + edges


class Ug(Graph):
    def __init__(self):
        Graph.__init__()

