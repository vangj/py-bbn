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
            parents = [bbn.get_node(parent_id) for parent_id in bbn.get_parents_ordered(node.id)]
            potential = PotentialUtil.get_potential(node, parents)
            node.potential = potential

    @staticmethod
    def reinit(jt):
        """
        Reinitialize potentials of BBN nodes in join tree.

        :param jt: Join tree.
        :return: None.
        """
        for node, parents in jt.get_bbn_node_and_parents().items():
            potential = PotentialUtil.get_potential(node, parents)
            node.potential = potential
