import numpy as np
import pandas as pd
from nose import with_setup
from numpy.testing import assert_almost_equal

from pybbn.graph.dag import BbnUtil, Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.jointree import EvidenceBuilder
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController
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
    """
    Tests creating table without parent.
    :return: None.
    """
    a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
    table = Table(a)

    assert not table.has_parents()
    assert_almost_equal(table.probs, np.array([0.5, 1.0]))
    assert 'on' == table.get_value(0.4)
    assert 'off' == table.get_value(0.6)


@with_setup(setup, teardown)
def test_pa_ch_table():
    """
    Tests create table with a single parent.
    :return: None.
    """
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
def test_multiple_pa_ch_table():
    """
    Tests create table with multiple parent.
    :return: None.
    """
    d_probs = [0.23323615160349853, 0.7667638483965015,
               0.7563025210084033, 0.24369747899159663]
    r_probs = [0.31000000000000005, 0.69,
               0.27, 0.73,
               0.13, 0.87,
               0.06999999999999995, 0.93]
    g_probs = [0.49, 0.51]

    g = BbnNode(Variable(0, 'gender', ['female', 'male']), g_probs)
    d = BbnNode(Variable(1, 'drug', ['false', 'true']), d_probs)
    r = BbnNode(Variable(2, 'recovery', ['false', 'true']), r_probs)

    table = Table(r, parents=[d, g])

    assert table.has_parents()
    lhs = np.array(list(table.probs.values()))
    rhs = np.array([[0.31, 1.0], [0.27, 1.0], [0.13, 1.0], [0.07, 1.0]])
    assert_almost_equal(lhs, rhs)

    lhs = list(table.probs.keys())
    rhs = ['0=female,1=false', '0=female,1=true', '0=male,1=false', '0=male,1=true']
    assert len(lhs) == len(rhs)
    for l, r in zip(lhs, rhs):
        assert l == r


@with_setup(setup, teardown)
def test_toplogical_sort_huang():
    """
    Tests toplogical sorting of Huang graph.
    """
    bbn = BbnUtil.get_huang_graph()
    sampler = LogicSampler(bbn)

    assert_almost_equal([0, 1, 2, 3, 4, 5, 6, 7], sampler.nodes)


@with_setup(setup, teardown)
def test_toplogical_sort_reversed():
    """
    Tests topological sorting of graph with nodes in reverse order.
    :return: None.
    """
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
    """
    Tests topological sort of diverging structure.
    :return: None.
    """
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
    """
    Tests sampler creation of tables.
    :return: None.
    """
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
    """
    Tests sampling a serial graph.
    :return: None.
    """
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

    s_a = s_a.sort_index()
    s_b = s_b.sort_index()
    s_c = s_c.sort_index()

    assert_almost_equal(s_a.values, np.array([0.4985, 0.5015]))
    assert_almost_equal(s_b.values, np.array([0.5502, 0.4498]))
    assert_almost_equal(s_c.values, np.array([0.5721, 0.4279]))

    join_tree = InferenceController.apply(bbn)
    posteriors = join_tree.get_posteriors()

    assert_almost_equal(s_a.values, np.array([posteriors['a']['off'], posteriors['a']['on']]), decimal=1)
    assert_almost_equal(s_b.values, np.array([posteriors['b']['off'], posteriors['b']['on']]), decimal=1)
    assert_almost_equal(s_c.values, np.array([posteriors['c']['off'], posteriors['c']['on']]), decimal=1)


@with_setup(setup, teardown)
def test_sampling_with_rejection():
    """
    Tests sampling a serial graph with rejection and evidence set.
    :return: None.
    """
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

    join_tree = InferenceController.apply(bbn)
    ev = EvidenceBuilder() \
        .with_node(join_tree.get_bbn_node_by_name('a')) \
        .with_evidence('on', 1.0) \
        .build()
    join_tree.set_observation(ev)
    posteriors = join_tree.get_posteriors()

    assert_almost_equal(s_a, np.array([posteriors['a']['on']]), decimal=1)
    assert_almost_equal(s_b, np.array([posteriors['b']['off'], posteriors['b']['on']]), decimal=1)
    assert_almost_equal(s_c, np.array([posteriors['c']['off'], posteriors['c']['on']]), decimal=1)
