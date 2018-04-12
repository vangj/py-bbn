from nose import with_setup

from pybbn.graph.dag import BbnUtil
from pybbn.pptc.initializer import Initializer
from pybbn.pptc.moralizer import Moralizer
from pybbn.pptc.potentialinitializer import PotentialInitializer
from pybbn.pptc.propagator import Propagator
from pybbn.pptc.transformer import Transformer
from pybbn.pptc.triangulator import Triangulator


def setup():
    """
    Setup.
    :return: None.
    """
    pass


def teardown():
    """
    Teardown.
    :return: None.
    """
    pass


@with_setup(setup, teardown)
def test_propagator():
    """
    Tests propagation.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()
    PotentialInitializer.init(bbn)

    ug = Moralizer.moralize(bbn)
    cliques = Triangulator.triangulate(ug)

    join_tree = Transformer.transform(cliques)

    Initializer.initialize(join_tree)
    Propagator.propagate(join_tree)

    # assert later
    # for clique in join_tree.get_cliques():
    #     potential = join_tree.potentials[clique.id]
    #     print(clique)
    #     print(potential)
    #     total = sum([entry.value for entry in potential.entries])
    #     print('total {}'.format(total))
    # assert 1 == 2
