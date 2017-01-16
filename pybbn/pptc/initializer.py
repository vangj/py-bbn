from pybbn.graph.potential import PotentialUtil


class Initializer:
    @staticmethod
    def initialize(join_tree):
        for clique in join_tree.get_cliques():
            potential = PotentialUtil.get_potential_from_nodes(clique.nodes)
            join_tree.add_potential(clique, potential)

        for sep_set in join_tree.get_sep_sets():
            potential = PotentialUtil.get_potential_from_nodes(sep_set.nodes)
            join_tree.add_potential(sep_set, potential)

        nodes = join_tree.get_bbn_nodes()
        for node in nodes:
            clique = Initializer.get_clique(node, join_tree)
            p1 = join_tree.potentials[clique.id]
            p2 = node.potential
            PotentialUtil.multiply(p1, p2)

        for node in nodes:
            for value in node.variable.values:
                clique = node.metadata['parent.clique']
                clique_potential = join_tree.potentials[clique.id]
                node_potential = join_tree.get_evidence(node, value)
                PotentialUtil.multiply(clique_potential, node_potential)

        return join_tree

    @staticmethod
    def get_clique(node, join_tree):
        if 'parent.clique' not in node.metadata:
            clique = join_tree.find_cliques_with_node_and_parents(node.id)[0]
            node.add_metadata('parent.clique', clique)
            return clique
        else:
            return node.metadata['parent.clique']