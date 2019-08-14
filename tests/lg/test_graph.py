import numpy as np
import pandas as pd
from nose import with_setup
from nose.tools import assert_almost_equal
from numpy.random import normal

from pybbn.lg.graph import Dag, Parameters, Bbn


def setup():
    """
    Setup.
    :return: None.
    """
    np.random.seed(37)


def teardown():
    """
    Teardown.
    :return: None.
    """
    pass


@with_setup(setup, teardown)
def test_create_dag():
    """
    Tests creating a basic dag.
    :return: None.
    """
    dag = Dag()
    dag.add_node(0)
    dag.add_node(1)
    dag.add_edge(0, 1)

    assert dag.number_of_nodes() == 2
    assert dag.number_of_edges() == 1
    assert 0 in dag.nodes()
    assert 1 in dag.nodes()
    assert (0, 1) in dag.edges()
    assert 0 == len(dag.parents(0))
    assert 1 == len(dag.children(0))
    assert 1 == len(dag.parents(1))
    assert 0 == len(dag.children(1))
    assert [0, 1] == dag.get_sorted_topology()


@with_setup(setup, teardown)
def test_create_dag_with_cycle():
    """
    Tests creating a DAG with a cycle.
    :return: None.
    """
    try:
        dag = Dag()
        dag.add_node(0)
        dag.add_node(1)
        dag.add_edge(0, 1)
        dag.add_edge(1, 0)

        assert True is False
    except ValueError:
        assert True is True


@with_setup(setup, teardown)
def test_markov_blanket():
    """
    Tests getting Markov blanket.
    :return: None.
    """
    g = Dag()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_node(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(3, 2)

    blanket = g.markov_blanket(1)
    assert 3 == len(blanket)
    assert 0 in blanket
    assert 2 in blanket
    assert 3 in blanket


@with_setup(setup, teardown)
def test_create_parameters():
    """
    Tests creating parameters.
    :return: None.
    """
    try:
        Parameters(np.array([0, 0]), np.array([[0, 0], [0, 0]]))
        assert True is True
    except ValueError:
        assert True is False


@with_setup(setup, teardown)
def test_create_parameter_means_not_eq_cov():
    """
    Tests creating parameters where means is not equal to covariance.
    :return: None.
    """
    try:
        Parameters(np.array([0, 0, 0]), np.array([[0, 0], [0, 0]]))
        assert True is False
    except ValueError:
        assert True is True


@with_setup(setup, teardown)
def test_create_parameter_cov_not_square():
    """
    Tests creating parameters where covariance matrix is not square.
    :return: None.
    """
    try:
        Parameters(np.array([0, 0]), np.array([[0, 0], [0, 0, 0]]))
        assert True is False
    except ValueError:
        assert True is True
    except IndexError:
        assert True is True


@with_setup(setup, teardown)
def test_create_bbn():
    """
    Tests creating a BBN.
    :return: None.
    """
    dag = Dag()
    dag.add_node(0)
    dag.add_node(1)
    dag.add_edge(0, 1)

    params = Parameters(np.array([1, 25]), np.array([[1, 2], [2, 4]]))

    bbn = Bbn(dag, params)
    assert bbn is not None

    try:
        dag = Dag()
        dag.add_node(0)

        params = Parameters(np.array([1, 25]), np.array([[1, 2], [2, 4]]))

        Bbn(dag, params)
        assert True is False
    except ValueError:
        assert True is True

    try:
        dag = Dag()
        dag.add_node(1)
        dag.add_node(2)
        dag.add_edge(1, 2)

        params = Parameters(np.array([1, 25]), np.array([[1, 2], [2, 4]]))

        Bbn(dag, params)
        assert True is False
    except ValueError:
        assert True is True

    try:
        dag = Dag()
        dag.add_node(0)
        dag.add_node(2)
        dag.add_edge(0, 2)

        params = Parameters(np.array([1, 25]), np.array([[1, 2], [2, 4]]))

        Bbn(dag, params)
        assert True is False
    except ValueError:
        assert True is True


@with_setup(setup, teardown)
def test_inference():
    """
    Tests inference.
    :return: None.
    """
    dag = Dag()
    dag.add_node(0)
    dag.add_node(1)
    dag.add_edge(0, 1)

    means = np.array([0, 25])
    cov = np.array([
        [1.09, 1.95],
        [1.95, 4.52]
    ])
    params = Parameters(means, cov)

    bbn = Bbn(dag, params)

    s, _ = bbn.do_inference()
    assert_almost_equal(s[0], 0.0, delta=0.01)
    assert_almost_equal(s[1], 25.0, delta=1.0)
    print(s)

    bbn.set_evidence(0, 1)
    s, _ = bbn.do_inference()
    assert_almost_equal(s[0], 1.0, delta=0.00)
    assert_almost_equal(s[1], 26.0, delta=1.0)
    print(s)
    bbn.clear_evidences()

    bbn.set_evidence(1, 20)
    s, _ = bbn.do_inference()
    assert_almost_equal(s[0], -2.0, delta=0.5)
    assert_almost_equal(s[1], 20.0, delta=0.0)
    print(s)
    bbn.clear_evidences()


@with_setup(setup, teardown)
def test_local_inference():
    """
    Tests local inference.
    :return: None.
    """
    dag = Dag()
    dag.add_node(0)
    dag.add_node(1)
    dag.add_edge(0, 1)

    means = np.array([0, 25])
    cov = np.array([
        [1.09, 1.95],
        [1.95, 4.52]
    ])
    params = Parameters(means, cov)

    bbn = Bbn(dag, params)

    s, _ = bbn.do_inference()
    assert_almost_equal(s[0], 0.0, delta=0.01)
    assert_almost_equal(s[1], 25.0, delta=1.0)
    print(s)

    bbn.set_evidence(0, 1)
    s, _ = bbn.do_inference()
    assert_almost_equal(s[0], 1.0, delta=0.00)
    assert_almost_equal(s[1], 25.0, delta=1.0)
    print(s)
    bbn.clear_evidences()

    bbn.set_evidence(1, 20)
    s, _ = bbn.do_inference()
    assert_almost_equal(s[0], -2.0, delta=0.5)
    assert_almost_equal(s[1], 20.0, delta=0.0)
    print(s)
    bbn.clear_evidences()


@with_setup(setup, teardown)
def test_sampled_mean_cov():
    """
    Tests getting sampled means and covariances.
    :return: None.
    """
    N = 10000

    x0 = normal(2.0, 1, N)
    x1 = normal(5.0 + 2.0 * x0, 1, N)
    x2 = normal(2.0, 1.0, N)
    x3 = normal(1.0 + 0.3 * x1 + 0.5 * x2, 1, N)
    x4 = normal(8.0 + 0.9 * x3, 1, N)

    X = np.hstack([x0.reshape(-1, 1), x1.reshape(-1, 1), x2.reshape(-1, 1), x3.reshape(-1, 1), x4.reshape(-1, 1)])
    M_e = X.mean(axis=0)
    S_e = np.cov(X.T)
    print(M_e)
    print('>')
    print(S_e)

    params = Parameters(M_e, S_e)

    dag = Dag()
    dag.add_node(0)
    dag.add_node(1)
    dag.add_node(2)
    dag.add_node(3)
    dag.add_node(4)
    dag.add_edge(0, 1)
    dag.add_edge(1, 3)
    dag.add_edge(2, 3)
    dag.add_edge(3, 4)
    bbn = Bbn(dag, params)

    M_o, S_o = bbn.do_inference(N=10000)
    print('>')
    print(M_o)
    print('>')
    print(S_o)

    assert M_e.shape[0] == M_o.shape[0]
    for e, o in zip(M_e, M_o):
        assert_almost_equal(e, o, delta=0.1)

    assert S_e.shape[0] == S_o.shape[0]
    assert S_e.shape[1] == S_o.shape[1]

    for r in range(S_e.shape[0]):
        for c in range(S_e.shape[1]):
            assert_almost_equal(S_e[r, c], S_o[r, c], delta=0.1)


@with_setup(setup, teardown)
def test_log_proba():
    """
    Tests log probability of data given a BBN.
    :return: None.
    """

    num_samples = 10000

    x0 = 2.0 + np.random.standard_normal(num_samples)
    x1 = 5.0 + 2.0 * x0 + np.random.standard_normal(num_samples)
    x2 = 2.0 + np.random.standard_normal(num_samples)
    x3 = 1.0 + 0.3 * x1 + 0.5 * x2 + np.random.standard_normal(num_samples)
    x4 = 8.0 + 0.9 * x3 + np.random.standard_normal(num_samples)

    df = pd.DataFrame({
        'x0': x0,
        'x1': x1,
        'x2': x2,
        'x3': x3,
        'x4': x4})
    X = df.values

    means = np.array(df.mean())
    cov = np.array(df.cov().values)

    params = Parameters(means, cov)

    dag1 = Dag()
    dag1.add_node(0)
    dag1.add_node(1)
    dag1.add_node(2)
    dag1.add_node(3)
    dag1.add_node(4)
    dag1.add_edge(0, 1)
    dag1.add_edge(1, 3)
    dag1.add_edge(2, 3)
    dag1.add_edge(3, 4)
    bbn1 = Bbn(dag1, params)
    lp1 = bbn1.log_prob(X)

    dag2 = Dag()
    dag2.add_node(0)
    dag2.add_node(1)
    dag2.add_node(2)
    dag2.add_node(3)
    dag2.add_node(4)
    dag2.add_edge(0, 1)
    dag2.add_edge(1, 3)
    dag2.add_edge(1, 4)
    dag2.add_edge(2, 3)
    bbn2 = Bbn(dag2, params)
    lp2 = bbn2.log_prob(df.values)

    dag3 = Dag()
    dag3.add_node(0)
    dag3.add_node(1)
    dag3.add_node(2)
    dag3.add_node(3)
    dag3.add_node(4)
    dag3.add_edge(0, 1)
    dag3.add_edge(1, 3)
    dag3.add_edge(3, 4)
    dag3.add_edge(3, 2)
    bbn3 = Bbn(dag3, params)
    lp3 = bbn3.log_prob(X)

    dag4 = Dag()
    dag4.add_node(0)
    dag4.add_node(1)
    dag4.add_node(2)
    dag4.add_node(3)
    dag4.add_node(4)
    dag4.add_edge(0, 1)
    dag4.add_edge(2, 3)
    dag4.add_edge(3, 4)
    bbn4 = Bbn(dag4, params)
    lp4 = bbn4.log_prob(X)

    print('lp1 {}'.format(lp1))
    print('lp2 {}'.format(lp2))
    print('lp3 {}'.format(lp3))
    print('lp4 {}'.format(lp4))

    assert lp1 > lp2
    assert lp1 > lp3
    assert lp1 > lp4

    logp1 = bbn1.predict_log_proba(X)
    logp2 = bbn2.predict_log_proba(X)
    logp3 = bbn3.predict_log_proba(X)
    logp4 = bbn4.predict_log_proba(X)

    assert len(logp1) == len(X)
    assert len(logp2) == len(X)
    assert len(logp3) == len(X)
    assert len(logp4) == len(X)

    assert_almost_equal(lp1, logp1.sum(), delta=0.001)
    assert_almost_equal(lp2, logp2.sum(), delta=0.001)
    assert_almost_equal(lp3, logp3.sum(), delta=0.001)
    assert_almost_equal(lp4, logp4.sum(), delta=0.001)

    p1 = bbn1.predict_proba(X)
    p2 = bbn2.predict_proba(X)
    p3 = bbn3.predict_proba(X)
    p4 = bbn4.predict_proba(X)

    assert len(p1) == len(X)
    assert len(p2) == len(X)
    assert len(p3) == len(X)
    assert len(p4) == len(X)

    assert_almost_equal(np.log10(p1).sum(), logp1.sum(), delta=0.001)
    assert_almost_equal(np.log10(p2).sum(), logp2.sum(), delta=0.001)
    assert_almost_equal(np.log10(p3).sum(), logp3.sum(), delta=0.001)
    assert_almost_equal(np.log10(p4).sum(), logp4.sum(), delta=0.001)
