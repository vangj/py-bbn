from pybbn.graph.graph import Ug
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.node import Clique


class Triangulator:
    @staticmethod
    def triangulate(m):
        cliques = []
        mm = Triangulator.duplicate(m)
        while len(mm.get_nodes()) > 0:
            node_clique = Triangulator.select_node(mm)
            clique = Clique(node_clique.get_bbn_nodes)

            if not Triangulator.is_subset(cliques, clique):
                cliques.append(clique)

            mm.remove_node(node_clique.node.id)

            for edge in node_clique.edges:
                m.add_edge(edge)
                mm.add_edge(edge)

        return cliques

    @staticmethod
    def duplicate(g):
        ug = Ug()
        for node in g.get_nodes():
            ug.add_node(node)
        for edge in g.get_edges():
            ug.add_edge(edge)
        return ug

    @staticmethod
    def select_node(m):
        cliques = []
        for node in m.get_nodes():
            weight = Triangulator.get_weight(node, m)
            edges = Triangulator.get_edges_to_add(node, m)
            neighbors = [m.get_node(i) for i in m.get_neighbors(i)]
            cliques.append(NodeClique(node, neighbors, weight, edges))
        cliques = sorted(cliques, key=lambda x: (len(x.edges), x.weight, x.node.id))
        return cliques[0]

    @staticmethod
    def get_weight(n, m):
        weight = n.get_weight()
        for neighbor_id in m.get_neighbors(n.id):
            neighbor = m.get_node(neighbor_id)
            weight *= neighbor.get_weight()
        return weight

    @staticmethod
    def get_edges_to_add(n, m):
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
        for i in len(cliques):
            if cliques[i].is_superset(clique):
                return True
        return False


class NodeClique:
    def __init__(self, node, neighbors, weight, edges):
        self.node = node
        self.neighbors = neighbors
        self.weight = weight
        self.edges = edges

    def get_bbn_nodes(self):
        nodes = [node for node in self.nodes]
        nodes.append(self.node)
        return nodes
