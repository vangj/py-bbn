from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.graph import Ug


class Moralizer(object):
    """
    Graph moralizer for a DAG.
    """

    @staticmethod
    def moralize(dag):
        """
        Moralizes a DAG.
        :param dag: DAG.
        :return: Moralized (undirected) graph.
        """
        ug = Ug()
        for node in dag.get_nodes():
            ug.add_node(node)
        for edge in dag.get_edges():
            ug.add_edge(Edge(edge.i, edge.j, EdgeType.UNDIRECTED))
        for node in dag.get_nodes():
            parents = [dag.get_node(pa) for pa in dag.get_parents(node.id)]
            size = len(parents)
            for i in range(size):
                pa1 = parents[i]
                for j in range(i + 1, size):
                    pa2 = parents[j]
                    ug.add_edge(Edge(pa1, pa2, EdgeType.UNDIRECTED))
        for node in dag.get_nodes():
            parents = [dag.get_node(pa) for pa in dag.get_parents(node.id)]
            node.add_metadata('parents', parents)

        return ug
