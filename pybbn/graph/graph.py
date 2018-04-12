from pybbn.graph.edge import EdgeType


class Graph(object):
    """
    Graph.
    """

    def __init__(self):
        """
        Ctor.
        """
        self.nodes = dict()
        self.edges = dict()
        self.map = dict()

    def get_neighbors(self, id):
        """
        Gets the neighbors of the specified node.
        :param id: Node id.
        :return: Set of neighbors of the specified node.
        """
        set1 = set([x for x in self.map[id]])
        set2 = set([x for x in self.map if id in self.map[x]])
        return set1 | set2

    def get_node(self, id):
        """
        Gets the node associated with the specified id.
        :param id: Node id.
        :return: Node.
        """
        return self.nodes[id]

    def get_nodes(self):
        """
        Gets all the nodes.
        :return: List of nodes.
        """
        return [node for node in self.nodes.values()]

    def get_edges(self):
        """
        Gets all the edges.
        :return: List of edges.
        """
        return [edge for edge in self.edges.values()]

    def add_node(self, node):
        """
        Adds a node.
        :param node: Node.
        :return: This graph.
        """
        self.nodes[node.id] = node
        return self

    def add_edge(self, edge):
        """
        Adds an edge.
        :param edge: Edge.
        :return: This graph.
        """
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

        return self

    def __shouldadd__(self, edge):
        """
        Checks if the specified edge should be added.
        :param edge: Edge.
        :return: A boolean indicating if the edge should be added.
        """
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
        """
        Checks if the specified edge id1 -- id2 exists.
        :param id1: Node id.
        :param id2: Node id.
        :return: A boolean indicating if the specified edge exists.
        """
        if id1 in self.map and id2 in self.map[id1]:
            return True
        if id2 in self.map and id1 in self.map[id2]:
            return True
        return False

    def remove_node(self, id):
        """
        Removes a node from the graph.
        :param id: Node id.
        """
        self.nodes.pop(id, None)
        self.map.pop(id, None)
        for k, v in self.map.items():
            if id in v:
                v.remove(id)

    def __str__(self):
        nodes = str.join('\n', [x.__str__() for x in self.nodes.values()])
        edges = str.join('\n', [x.__str__() for x in self.edges.values()])
        return nodes + '\n' + edges


class Ug(Graph):
    """
    Undirected graph.
    """

    def __init__(self):
        """
        Ctor.
        """
        Graph.__init__(self)
