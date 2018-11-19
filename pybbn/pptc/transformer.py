from pybbn.graph.edge import JtEdge
from pybbn.graph.jointree import JoinTree
from pybbn.graph.node import SepSet


class Transformer(object):
    """
    Transformer. Transforms a list of cliques into a join tree.
    """

    @staticmethod
    def transform(cliques):
        """
        Transforms the cliques into a join tree.
        :param cliques: List of cliques.
        :return: Join tree.
        """
        join_tree = JoinTree()
        sep_sets = Transformer.get_sep_sets(cliques)

        for i in range(len(sep_sets)):
            join_tree.add_edge(JtEdge(sep_sets[i]))

        return join_tree

    @staticmethod
    def get_sep_sets(cliques):
        """
        Gets all pair-wise separation-sets.
        :param cliques: Array of cliques.
        :return: Array of separation sets sorted descendingly by mass followed by
        cost (asc) and id (asc).
        """
        sep_sets = []
        size = len(cliques)
        for i in range(size):
            clique_i = cliques[i]
            for j in range(i + 1, size):
                clique_j = cliques[j]
                sep_set = SepSet(clique_i, clique_j)
                if sep_set.is_empty is False:
                    sep_sets.append(sep_set)
        return sorted(sep_sets, key=lambda x: (-1 * x.mass, x.cost, x.id))
