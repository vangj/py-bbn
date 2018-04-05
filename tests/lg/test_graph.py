import numpy as np
from nose import with_setup

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
    Test inference.
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

    bbn = Bbn(dag, params, max_samples=2000, max_iters=10)

    s = bbn.do_inference()
    print(s)

    bbn.set_evidence(0, 1)
    s = bbn.do_inference()
    print(s)
    bbn.clear_evidences()

    bbn.set_evidence(1, 20)
    s = bbn.do_inference()
    print(s)
    bbn.clear_evidences()
