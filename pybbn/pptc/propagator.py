from pybbn.pptc.evidencecollector import EvidenceCollector
from pybbn.pptc.evidencedistributor import EvidenceDistributor


class Propagator(object):
    """
    Evidence propagator.
    """

    @staticmethod
    def propagate(join_tree):
        """
        Propagates evidence.
        :param join_tree: Join tree.
        :return: Join tree.
        """
        cliques = sorted(join_tree.get_cliques(), key=lambda c: c.id)
        x = cliques[0]
        # print(x)

        join_tree.unmark_cliques()
        Propagator.collect_evidence(join_tree, x)

        join_tree.unmark_cliques()
        Propagator.distribute_evidence(join_tree, x)

        return join_tree

    @staticmethod
    def collect_evidence(join_tree, start):
        """
        Collects evidence.
        :param join_tree: Join tree.
        :param start: Start clique.
        """
        collector = EvidenceCollector(join_tree, start)
        collector.start()

    @staticmethod
    def distribute_evidence(join_tree, start):
        """
        Distributes evidence.
        :param join_tree: Join tree.
        :param start: Start clique.
        """
        distributor = EvidenceDistributor(join_tree, start)
        distributor.start()
