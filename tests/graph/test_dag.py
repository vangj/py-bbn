from nose import with_setup

from pybbn.graph.dag import Dag
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.node import Node


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
def test_dag_creation():
    """
    Tests DAG creation.
    :return: None.
    """
    n0 = Node(0)
    n1 = Node(1)
    n2 = Node(2)
    e0 = Edge(n0, n1, EdgeType.DIRECTED)
    e1 = Edge(n1, n2, EdgeType.DIRECTED)
    e2 = Edge(n2, n0, EdgeType.DIRECTED)

    g = Dag()
    g.add_node(n0)
    g.add_node(n1)
    g.add_edge(e0)
    g.add_edge(e1)
    g.add_edge(e2)

    print(g)

    assert len(g.get_nodes()) == 3
    assert len(g.get_edges()) == 2

    assert len(list(g.get_neighbors(0))) == 1
    assert len(list(g.get_neighbors(1))) == 2
    assert len(list(g.get_neighbors(2))) == 1

    assert 1 in g.get_neighbors(0)
    assert 0 in g.get_neighbors(1)
    assert 2 in g.get_neighbors(1)
    assert 1 in g.get_neighbors(2)

    assert g.edge_exists(0, 1) == 1
    assert g.edge_exists(1, 2) == 1
    assert g.edge_exists(0, 2) == 0

    assert len(g.get_parents(0)) == 0
    assert len(g.get_parents(1)) == 1
    assert len(g.get_parents(2)) == 1

    assert 0 in g.get_parents(1)
    assert 1 in g.get_parents(2)

    assert len(g.get_children(0)) == 1
    assert len(g.get_children(1)) == 1
    assert len(g.get_children(2)) == 0

    assert 1 in g.get_children(0)
    assert 2 in g.get_children(1)
