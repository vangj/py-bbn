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

    e_edges = set([
        '0--1',
        '0--2',
        '1--3',
        '2--4',
        '3--5',
        '4--5',
        '2--6',
        '4--7',
        '6--7',
        '3--4',
        '4--6'
    ])

    o_edges = set([str(edge) for edge in ug.get_edges()])

    assert len(e_edges) == len(o_edges)
    for e in e_edges:
        assert e in o_edges
