from nose import with_setup
from pybbn.generator.bbngenerator import generate_singly_bbn, generate_multi_bbn


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
    Test generating singly-connected BBN.
    :return: None.
    """
    g, p = generate_singly_bbn(3)

    assert len(g.nodes) == 3
    assert len(g.edges) == 2


@with_setup(setup, teardown)
def test_multi_connected():
    """
    Test generating multi-connected BBN.
    :return: None.
    """
    g, p = generate_multi_bbn(4)

    assert len(g.nodes) == 4
    assert len(g.edges) > 1