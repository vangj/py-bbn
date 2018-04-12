from nose import with_setup

from pybbn.graph.dag import BbnUtil
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
def test_potential_initializer():
    """
    Tests potential initialization.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()
    PotentialInitializer.init(bbn)

    # assert later
    # for node in bbn.get_nodes():
    #     potential = node.potential
    #     print('{} {}'.format(node.id, node.variable.name))
    #     print(potential)
    #
    # assert 1 == 2
