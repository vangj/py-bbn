from nose import with_setup
import numpy as np
from numpy.testing import assert_almost_equal

from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.sampling.sampling import Table


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
def test_table():
    a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
    table = Table(a)

    assert not table.has_parents()
    assert_almost_equal(table.probs, np.array([0.5, 1.0]))
