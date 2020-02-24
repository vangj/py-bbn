import copy

from nose import with_setup

from pybbn.graph.edge import Edge, EdgeType


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
def test_copy():
    """
    Tests edge copy.
    :return: None.
    """
    lhs = Edge(0, 1, EdgeType.UNDIRECTED)
    rhs = copy.copy(lhs)

    assert lhs.i == rhs.i
    assert lhs.j == rhs.j
    assert lhs.type == rhs.type


@with_setup(setup, teardown)
def test_deepcopy():
    """
    Tests edge deep copy.
    :return: None.
    """
    lhs = Edge(0, 1, EdgeType.UNDIRECTED)
    rhs = copy.deepcopy(lhs)

    assert lhs.i == rhs.i
    assert lhs.j == rhs.j
    assert lhs.type == rhs.type

    lhs.i = 3
    assert lhs.i != rhs.i
