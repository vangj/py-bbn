from pybbn.graph.jointree import JoinTree
from pybbn.graph.node import SepSet
from pybbn.graph.edge import JtEdge


class Transformer:
    @staticmethod
    def transform(cliques):
        join_tree = JoinTree()
        sep_sets = Transformer.get_sep_sets(cliques)
        n = (len(cliques) - 1) * 2
        total = 0

        for i in range(len(sep_sets)):
            join_tree.add_edge(JtEdge(sep_sets[i]))
            total += 2
            if total == n:
                break

        return join_tree

    @staticmethod
    def get_sep_sets(cliques):
        sep_sets = []
        size = len(cliques)
        for i in range(size):
            for j in range(i + 1, size):
                sep_set = SepSet(cliques[i], cliques[j])
                sep_sets.append(sep_set)
        return sorted(sep_sets, key=lambda x: (-1 * x.mass, x.cost, x.id))
