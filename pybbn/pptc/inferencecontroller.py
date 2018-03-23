from pybbn.graph.jointree import JoinTreeListener
from pybbn.pptc.initializer import Initializer
from pybbn.pptc.moralizer import Moralizer
from pybbn.pptc.potentialinitializer import PotentialInitializer
from pybbn.pptc.propagator import Propagator
from pybbn.pptc.transformer import Transformer
from pybbn.pptc.triangulator import Triangulator


class InferenceController(JoinTreeListener):
    """
    Inference controller.
    """

    @staticmethod
    def apply(bbn):
        """
        Sets up the specified BBN for probability propagation in tree clusters (PPTC).
        :param bbn: BBN graph.
        :return: Join tree.
        """
        PotentialInitializer.init(bbn)

        ug = Moralizer.moralize(bbn)
        cliques = Triangulator.triangulate(ug)
        join_tree = Transformer.transform(cliques)

        Initializer.initialize(join_tree)
        Propagator.propagate(join_tree)

        join_tree.set_listener(InferenceController())

        return join_tree

    def evidence_retracted(self, join_tree):
        """
        Evidence is retracted.
        :param join_tree: Join tree.
        """
        Initializer.initialize(join_tree)
        Propagator.propagate(join_tree)

    def evidence_updated(self, join_tree):
        """
        Evidence is updated.
        :param join_tree: Join tree.
        """
        Propagator.propagate(join_tree)
