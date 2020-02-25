from collections import defaultdict
from copy import deepcopy

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
        self.edge_map = defaultdict(set)
        self.neighbors = defaultdict(set)

    def get_neighbors(self, id):
        """
        Gets the neighbors of the specified node.

        :param id: Node id.
        :return: Set of neighbors of the specified node.
        """
        return self.neighbors[id]

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
        return self.nodes.values()

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
        if node.id not in self.nodes:
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

        if self.__shouldadd__(edge):
            self.edges[edge.key] = edge
            self.edge_map[edge.i.id].add(edge.j.id)
            if EdgeType.UNDIRECTED == edge.type:
                self.edge_map[edge.j.id].add(edge.i.id)

            self.neighbors[edge.i.id].add(edge.j.id)
            self.neighbors[edge.j.id].add(edge.i.id)

            self.__edge_added__(edge)

        return self

    def __edge_added__(self, edge):
        """
        Callback listener for sub-classes when an edge has been added.

        :param edge: Edge.
        :return: None.
        """
        pass

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
            if lhs.id not in self.edge_map[rhs.id] or rhs.id not in self.edge_map[lhs.id]:
                return True
        else:
            if rhs.id not in self.edge_map[lhs.id]:
                return True

        return False

    def edge_exists(self, id1, id2):
        """
        Checks if the specified edge id1 -- id2 exists.

        :param id1: Node id.
        :param id2: Node id.
        :return: A boolean indicating if the specified edge exists.
        """
        if id1 in self.edge_map and id2 in self.edge_map[id1]:
            return True
        if id2 in self.edge_map and id1 in self.edge_map[id2]:
            return True
        return False

    def remove_node(self, id):
        """
        Removes a node from the graph.

        :param id: Node id.
        """
        self.nodes.pop(id, None)
        self.edge_map.pop(id, None)
        self.neighbors.pop(id, None)

        for k, v in self.edge_map.items():
            if id in v:
                v.remove(id)

        for k, v in self.neighbors.items():
            if id in v:
                v.remove(id)

    def __str__(self):
        nodes = str.join('\n', [x.__str__() for x in self.nodes.values()])
        edges = str.join('\n', [x.__str__() for x in self.edges.values()])
        return nodes + '\n' + edges

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memodict))
        return result


class Ug(Graph):
    """
    Undirected graph.
    """

    def __init__(self):
        """
        Ctor.
        """
        Graph.__init__(self)
