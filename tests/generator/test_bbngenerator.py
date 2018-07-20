from nose import with_setup

from pybbn.generator.bbngenerator import generate_singly_bbn, generate_multi_bbn, convert_for_exact_inference
from pybbn.generator.bbngenerator import convert_for_drawing


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
def test_singly_connected():
    """
    Tests generating singly-connected BBN.
    :return: None.
    """
    g, p = generate_singly_bbn(3)

    assert len(g.nodes) == 3
    assert len(g.edges) == 2


@with_setup(setup, teardown)
def test_multi_connected():
    """
    Tests generating multi-connected BBN.
    :return: None.
    """
    g, p = generate_multi_bbn(4)

    assert len(g.nodes) == 4
    assert len(g.edges) > 1


@with_setup(setup, teardown)
def test_convert_for_exact_inference():
    """
    Tests converting graph and params to a BBN.
    :return: None
    """

    g, p = generate_singly_bbn(2)
    bbn = convert_for_exact_inference(g, p)

    assert len(bbn.nodes) == 2
    assert len(bbn.edges) == 1


@with_setup(setup, teardown)
def test_convert_for_drawing():
    """
    Tests converting BBN to networkx DAG.
    :return: None
    """

    g, p = generate_singly_bbn(2)
    bbn = convert_for_exact_inference(g, p)

    graph = convert_for_drawing(bbn)
    nodes = list(graph.nodes)
    edges = list(graph.edges)

    assert len(nodes) == 2
    assert len(edges) == 1
