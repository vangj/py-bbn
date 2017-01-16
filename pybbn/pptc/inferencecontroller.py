from pybbn.pptc.potentialinitializer import PotentialInitializer
from pybbn.pptc.moralizer import Moralizer
from pybbn.pptc.triangulator import Triangulator
from pybbn.pptc.transformer import Transformer
from pybbn.pptc.initializer import Initializer
from pybbn.pptc.propagator import Propagator
from pybbn.graph.jointree import JoinTreeListener


class InferenceController(JoinTreeListener):
    @staticmethod
    def apply(bbn):
        PotentialInitializer.init(bbn)

        ug = Moralizer.moralize(bbn)
        cliques = Triangulator.triangulate(ug)
        join_tree = Transformer.transform(cliques)

        Initializer.initialize(join_tree)
        Propagator.propagate(join_tree)

        join_tree.set_listener(InferenceController())

        return join_tree

    def evidence_retracted(self, join_tree):
        Initializer.initialize(join_tree)
        Propagator.propagate(join_tree)

    def evidence_updated(self, join_tree):
        Propagator.propagate(join_tree)
