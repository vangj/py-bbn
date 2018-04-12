from pybbn.graph.potential import PotentialUtil


class PotentialInitializer(object):
    """
    Potential initializer.
    """

    @staticmethod
    def init(bbn):
        """
        Initializes the BBN potentials.
        :param bbn: BBN graph.
        """
        for node in bbn.get_nodes():
            parents = [bbn.get_node(parent_id) for parent_id in bbn.get_parents(node.id)]
            node.potential = PotentialUtil.get_potential(node, parents)
