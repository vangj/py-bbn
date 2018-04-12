from nose import with_setup

from pybbn.graph.dag import BbnUtil
from pybbn.pptc.moralizer import Moralizer
from pybbn.pptc.potentialinitializer import PotentialInitializer
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
def test_transformer():
    """
    Tests transformer.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()
    PotentialInitializer.init(bbn)

    ug = Moralizer.moralize(bbn)
    cliques = Triangulator.triangulate(ug)

    join_tree = Transformer.transform(cliques)

    # assert later
    # print(join_tree)
    # assert 1 == 2
