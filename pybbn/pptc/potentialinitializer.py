from pybbn.graph.potential import PotentialUtil


class PotentialInitializer:
    @staticmethod
    def init(bbn):
        for node in bbn.get_nodes():
            parents = [bbn.get_node(parent_id) for parent_id in bbn.get_parents(node.id)]
            node.potential = PotentialUtil.get_potential(node, parents)
