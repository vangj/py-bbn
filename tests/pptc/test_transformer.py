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

    e_nodes = set([
        '(d,e,f)',
        '(e,g,h)',
        '(c,e,g)',
        '(a,b,c)',
        '(b,c,d)',
        '(c,d,e)',
        '|(a,b,c) -- b,c -- (b,c,d)|',
        '|(b,c,d) -- c,d -- (c,d,e)|',
        '|(c,e,g) -- c,e -- (c,d,e)|',
        '|(d,e,f) -- d,e -- (c,d,e)|',
        '|(e,g,h) -- e,g -- (c,e,g)|'
    ])

    e_edges = set([
        '(a,b,c)--|(a,b,c) -- b,c -- (b,c,d)|--(b,c,d)',
        '(b,c,d)--|(b,c,d) -- c,d -- (c,d,e)|--(c,d,e)',
        '(c,e,g)--|(c,e,g) -- c,e -- (c,d,e)|--(c,d,e)',
        '(d,e,f)--|(d,e,f) -- d,e -- (c,d,e)|--(c,d,e)',
        '(e,g,h)--|(e,g,h) -- e,g -- (c,e,g)|--(c,e,g)'
    ])

    o_nodes = [str(n) for n in join_tree.get_nodes()]
    o_edges = [str(e) for e in join_tree.get_edges()]

    assert len(e_nodes) == len(o_nodes)
    for n in e_nodes:
        assert n in o_nodes

    assert len(e_edges) == len(o_edges)
    for e in e_edges:
        assert e in o_edges
