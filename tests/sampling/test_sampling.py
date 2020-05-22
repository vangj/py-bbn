from nose import with_setup
import numpy as np
import pandas as pd
from numpy.testing import assert_almost_equal

from pybbn.graph.dag import BbnUtil, Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.sampling.sampling import Table, LogicSampler


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
    assert 'on' == table.get_value(0.4)
    assert 'off' == table.get_value(0.6)


@with_setup(setup, teardown)
def test_pa_ch_table():
    a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
    b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
    table = Table(b, parents=[a])

    assert table.has_parents()
    lhs = np.array(list(table.probs.values()))
    rhs = np.array([[0.5, 1.0], [0.4, 1.0]])
    assert_almost_equal(lhs, rhs)
    assert 'on' == table.get_value(0.4, sample={0: 'on'})
    assert 'off' == table.get_value(0.7, sample={0: 'on'})
    assert 'on' == table.get_value(0.3, sample={0: 'off'})
    assert 'off' == table.get_value(0.6, sample={0: 'off'})


@with_setup(setup, teardown)
def test_toplogical_sort_huang():
    bbn = BbnUtil.get_huang_graph()
    sampler = LogicSampler(bbn)

    assert_almost_equal([0, 1, 2, 3, 4, 5, 6, 7], sampler.nodes)


@with_setup(setup, teardown)
def test_toplogical_sort_reversed():
    a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])
    b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
    c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.5, 0.5])

    bbn = Bbn() \
        .add_node(a) \
        .add_node(b) \
        .add_node(c) \
        .add_edge(Edge(c, b, EdgeType.DIRECTED)) \
        .add_edge(Edge(b, a, EdgeType.DIRECTED))

    sampler = LogicSampler(bbn)

    assert_almost_equal([2, 1, 0], sampler.nodes)


@with_setup(setup, teardown)
def test_toplogical_sort_mixed():
    a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])
    b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5])
    c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])

    bbn = Bbn() \
        .add_node(a) \
        .add_node(b) \
        .add_node(c) \
        .add_edge(Edge(b, a, EdgeType.DIRECTED)) \
        .add_edge(Edge(b, c, EdgeType.DIRECTED))

    sampler = LogicSampler(bbn)

    assert_almost_equal([1, 0, 2], sampler.nodes)


@with_setup(setup, teardown)
def test_sampler_tables():
    a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
    b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
    c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])

    bbn = Bbn() \
        .add_node(a) \
        .add_node(b) \
        .add_node(c) \
        .add_edge(Edge(a, b, EdgeType.DIRECTED)) \
        .add_edge(Edge(b, c, EdgeType.DIRECTED))

    sampler = LogicSampler(bbn)

    assert_almost_equal([0, 1, 2], sampler.nodes)

    tables = sampler.tables
    assert 3 == len(tables)
    assert 0 in tables
    assert 1 in tables
    assert 2 in tables

    lhs = np.array(tables[0].probs)
    rhs = np.array([0.5, 1.0])
    assert_almost_equal(lhs, rhs)

    lhs = np.array(list(tables[1].probs.values()))
    rhs = np.array([[0.5, 1.0], [0.4, 1.0]])
    assert_almost_equal(lhs, rhs)

    lhs = np.array(list(tables[2].probs.values()))
    rhs = np.array([[0.7, 1.0], [0.2, 1.0]])
    assert_almost_equal(lhs, rhs)


@with_setup(setup, teardown)
def test_sampling():
    a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
    b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
    c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])

    bbn = Bbn() \
        .add_node(a) \
        .add_node(b) \
        .add_node(c) \
        .add_edge(Edge(a, b, EdgeType.DIRECTED)) \
        .add_edge(Edge(b, c, EdgeType.DIRECTED))

    sampler = LogicSampler(bbn)

    n_samples = 10000
    samples = pd.DataFrame(sampler.get_samples(n_samples=n_samples, seed=37))
    samples.columns = ['a', 'b', 'c']

    assert n_samples == samples.shape[0]
    assert 3 == samples.shape[1]

    s_a = samples.a.value_counts()
    s_b = samples.b.value_counts()
    s_c = samples.c.value_counts()

    s_a = s_a / s_a.sum()
    s_b = s_b / s_b.sum()
    s_c = s_c / s_c.sum()

    s_a = s_a.sort_index().values
    s_b = s_b.sort_index().values
    s_c = s_c.sort_index().values

    assert_almost_equal(s_a, np.array([0.4985, 0.5015]))
    assert_almost_equal(s_b, np.array([0.5502, 0.4498]))
    assert_almost_equal(s_c, np.array([0.5721, 0.4279]))


@with_setup(setup, teardown)
def test_sampling_with_rejection():
    a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
    b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
    c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])

    bbn = Bbn() \
        .add_node(a) \
        .add_node(b) \
        .add_node(c) \
        .add_edge(Edge(a, b, EdgeType.DIRECTED)) \
        .add_edge(Edge(b, c, EdgeType.DIRECTED))

    sampler = LogicSampler(bbn)

    n_samples = 10000
    samples = pd.DataFrame(sampler.get_samples(evidence={0: 'on'}, n_samples=n_samples, seed=37))
    samples.columns = ['a', 'b', 'c']

    assert n_samples == samples.shape[0]
    assert 3 == samples.shape[1]

    s_a = samples.a.value_counts()
    s_b = samples.b.value_counts()
    s_c = samples.c.value_counts()

    s_a = s_a / s_a.sum()
    s_b = s_b / s_b.sum()
    s_c = s_c / s_c.sum()

    s_a = s_a.sort_index().values
    s_b = s_b.sort_index().values
    s_c = s_c.sort_index().values

    assert_almost_equal(s_a, np.array([1.0]))
    assert_almost_equal(s_b, np.array([0.5006, 0.4994]))
    assert_almost_equal(s_c, np.array([0.5521, 0.4479]))