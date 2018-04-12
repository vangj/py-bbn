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
    def select_node(m):
        """
        Selects a clique from the specified graph. Cliques are sorted by number of edges, weight, and id (asc).
        :param m: Graph.
        :return: Clique.
        """
        cliques = []
        for node in m.get_nodes():
            weight = Triangulator.get_weight(node, m)
            edges = Triangulator.get_edges_to_add(node, m)
            neighbors = [m.get_node(neighbor_id) for neighbor_id in m.get_neighbors(node.id)]
            cliques.append(NodeClique(node, neighbors, weight, edges))
        cliques = sorted(cliques, key=lambda x: (len(x.edges), x.weight, x.node.id))
        return cliques[0]

    @staticmethod
    def get_weight(n, m):
        """
        Gets the weight of a BBN node. The weight of a node is the product of the its weight with all its
        neighbors' weight.
        :param n: BBN node.
        :param m: Graph.
        :return: Weight.
        """
        weight = n.get_weight()
        for neighbor_id in m.get_neighbors(n.id):
            neighbor = m.get_node(neighbor_id)
            weight *= neighbor.get_weight()
        return weight

    @staticmethod
    def get_edges_to_add(n, m):
        """
        Gets edges to add.
        :param n: BBN node.
        :param m: Graph.
        :return: Array of edges.
        """
        edges = []
        neighbors = [m.get_node(i) for i in m.get_neighbors(n.id)]
        size = len(neighbors)
        for i in range(size):
            ne1 = neighbors[i]
            for j in range(i + 1, size):
                ne2 = neighbors[j]
                if not m.edge_exists(ne1.id, ne2.id):
                    edges.append(Edge(ne1, ne2, EdgeType.UNDIRECTED))
        return edges

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
        nodes = [node for node in self.neighbors]
        nodes.append(self.node)
        return nodes
