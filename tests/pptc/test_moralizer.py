from pybbn.graph.dag import BbnUtil
from pybbn.pptc.potentialinitializer import PotentialInitializer
from pybbn.pptc.moralizer import Moralizer
from nose import with_setup


def setup():
    pass


def teardown():
    pass


@with_setup(setup, teardown)
def test_moralizer():
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