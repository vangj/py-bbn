from nose import with_setup

from pybbn.graph.dag import BbnUtil
from pybbn.pptc.moralizer import Moralizer
from pybbn.pptc.potentialinitializer import PotentialInitializer


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
def test_moralizer():
    """
    Tests moralization.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()
    PotentialInitializer.init(bbn)

    ug = Moralizer.moralize(bbn)

    # assert later
    # for node in ug.get_nodes():
    #     print(node)
    # for edge in ug.get_edges():
    #     print(edge)
    #
    # assert 1 == 2
