from pybbn.pptc.evidencecollector import EvidenceCollector
from pybbn.pptc.evidencedistributor import EvidenceDistributor


class Propagator:
    @staticmethod
    def propagate(join_tree):
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
        collector = EvidenceCollector(join_tree, start)
        collector.start()

    @staticmethod
    def distribute_evidence(join_tree, start):
        distributor = EvidenceDistributor(join_tree, start)
        distributor.start()
