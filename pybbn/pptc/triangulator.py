from functools import reduce
from itertools import combinations

from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.graph import Ug
from pybbn.graph.node import Clique


class Triangulator(object):
    """
    Triangulator. Triangulates an undirected moralized graph and produces cliques in the process.
    """

    @staticmethod
    def triangulate(m):
        """
        Triangulates the specified moralized graph.

        :param m: Moralized undirected graph.
        :return: Array of cliques.
        """
        cliques = []
        mm = Triangulator.duplicate(m)
        while len(mm.get_nodes()) > 0:
            node_clique = Triangulator.select_node(mm)
            clique = Clique(node_clique.get_bbn_nodes())

            if not Triangulator.is_subset(cliques, clique):
                cliques.append(clique)

            mm.remove_node(node_clique.node.id)

            for edge in node_clique.edges:
                m.add_edge(edge)
                mm.add_edge(edge)

        return cliques

    @staticmethod
    def duplicate(g):
        """
        Duplicates a undirected graph.

        :param g: Undirected graph.
        :return: Undirected graph.
        """
        ug = Ug()
        for node in g.get_nodes():
            ug.add_node(node)
        for edge in g.get_edges():
            ug.add_edge(edge)
        return ug

    @staticmethod
    def generate_cliques(m):
        """
        Generates a list of node cliques.

        :param m: Graph.
        :return: List of NodeCliques.
        """

        def get_neighbors(node, m):
            return [m.get_node(neighbor_id) for neighbor_id in m.get_neighbors(node.id)]

        def get_weight(node, m):
            return Triangulator.get_weight(node, m)

        def get_edges_to_add(node, m):
            return Triangulator.get_edges_to_add(node, m)

        return (NodeClique(node, get_neighbors(node, m), get_weight(node, m), get_edges_to_add(node, m))
                for node in m.get_nodes())

    @staticmethod
    def select_node(m):
        """
        Selects a clique from the specified graph. Cliques are sorted by number of edges, weight, and id (asc).

        :param m: Graph.
        :return: Clique.
        """
        return sorted(Triangulator.generate_cliques(m), key=lambda x: (len(x.edges), x.weight, x.node.id))[0]

    @staticmethod
    def get_weight(n, m):
        """
        Gets the weight of a BBN node. The weight of a node is the product of the its weight with all its
        neighbors' weight.

        :param n: BBN node.
        :param m: Graph.
        :return: Weight.
        """
        if len(m.neighbors[n.id]) == 0:
            return n.get_weight()
        weights = (m.get_node(neighbor_id).get_weight() for neighbor_id in m.get_neighbors(n.id))
        return n.get_weight() * reduce(lambda x, y: x * y, weights)

    @staticmethod
    def get_edges_to_add(n, m):
        """
        Gets edges to add.

        :param n: BBN node.
        :param m: Graph.
        :return: Array of edges.
        """
        neighbors = [m.get_node(i) for i in m.get_neighbors(n.id)]
        return [Edge(neighbors[i], neighbors[j], EdgeType.UNDIRECTED)
                for i, j in combinations(range(len(neighbors)), 2)
                if not m.edge_exists(neighbors[i].id, neighbors[j].id)]

    @staticmethod
    def is_subset(cliques, clique):
        """
        Checks if the specified clique is a subset of the specified list of cliques.

        :param cliques: List of cliques.
        :param clique: Clique.
        :return: A boolean indicating if the clique is a subset.
        """
        for i in range(len(cliques)):
            if cliques[i].is_superset(clique):
                return True
        return False


class NodeClique:
    """
    Node clique.
    """

    def __init__(self, node, neighbors, weight, edges):
        """
        Ctor.

        :param node: BBN node.
        :param neighbors: BBN nodes (neighbors).
        :param weight: Weight.
        :param edges: Edges.
        """
        self.node = node
        self.neighbors = neighbors
        self.weight = weight
        self.edges = edges

    def get_bbn_nodes(self):
        """
        Gets all the BBN nodes in this node clique.

        :return: Array of BBN nodes.
        """
        neighbors = [node for node in self.neighbors] + [self.node]
        return neighbors

    def __str__(self):
        return f'{self.node.id}|weight={self.weight}|edges={len(self.edges)}|neighbors={len(self.neighbors)}'
