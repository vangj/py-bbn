from nose import with_setup

from pybbn.graph.dag import BbnUtil
from pybbn.pptc.moralizer import Moralizer
from pybbn.pptc.potentialinitializer import PotentialInitializer
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
def test_triangulator():
    """
    Tests triangulation.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()
    PotentialInitializer.init(bbn)

    ug = Moralizer.moralize(bbn)
    cliques = Triangulator.triangulate(ug)

    e_cliques = set([
        '(d,e,f)',
        '(e,g,h)',
        '(c,e,g)',
        '(a,b,c)',
        '(b,c,d)',
        '(c,d,e)'
    ])

    o_cliques = [str(c) for c in cliques]

    assert len(e_cliques) == len(o_cliques)
    for c in e_cliques:
        assert c in o_cliques
