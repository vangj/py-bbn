import copy

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
        join_tree.parent_info = {node.id: bbn.get_parents_ordered(node.id) for node in bbn.get_nodes()}

        Initializer.initialize(join_tree)
        Propagator.propagate(join_tree)

        join_tree.set_listener(InferenceController())

        return join_tree

    @staticmethod
    def reapply(join_tree, cpts):
        """
        Reapply propagation to join tree with new CPTs. The join tree structure is kept but the BBN node CPTs
        are updated. A new instance/copy of the join tree will be returned.

        :param join_tree: Join tree.
        :param cpts: Dictionary of new CPTs. Keys are id's of nodes and values are new CPTs.
        :return: Join tree.
        """
        jt = copy.deepcopy(join_tree)
        jt.update_bbn_cpts(cpts)
        jt.listener = None
        jt.evidences = dict()

        PotentialInitializer.reinit(jt)
        Initializer.initialize(jt)
        Propagator.propagate(jt)

        jt.set_listener(InferenceController())

        return jt

    @staticmethod
    def apply_from_serde(join_tree):
        """
        Applies propagation to join tree from a deserialzed join tree.

        :param join_tree: Join tree.
        :return: Join tree (the same one passed in).
        """
        join_tree.listener = None
        join_tree.evidences = dict()

        PotentialInitializer.reinit(join_tree)
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
