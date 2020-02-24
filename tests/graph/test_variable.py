import copy

from nose import with_setup

from pybbn.graph.variable import Variable


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
    Tests variable copy.
    :return: None.
    """
    lhs = Variable(0, 'a', ['t', 'f'])
    rhs = copy.copy(lhs)

    assert lhs.id == rhs.id
    assert lhs.name == rhs.name
    assert len(lhs.values) == len(rhs.values)
    for lhs_v, rhs_v in zip(lhs.values, rhs.values):
        assert lhs_v == rhs_v

    lhs.values[0] = 'true'
    assert lhs.values[0] == rhs.values[0]


@with_setup(setup, teardown)
def test_deep_copy():
    """
    Tests variable deepcopy.
    :return: None.
    """
    lhs = Variable(0, 'a', ['t', 'f'])
    rhs = copy.deepcopy(lhs)

    assert lhs.id == rhs.id
    assert lhs.name == rhs.name
    assert len(lhs.values) == len(rhs.values)
    for lhs_v, rhs_v in zip(lhs.values, rhs.values):
        assert lhs_v == rhs_v

    lhs.values[0] = 'true'
    assert lhs.values[0] != rhs.values[0]
