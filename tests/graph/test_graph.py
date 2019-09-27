import copy

from nose import with_setup

from pybbn.graph.dag import Dag
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.graph import Graph, Ug
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
def test_graph_creation():
    """
    Tests graph creation.
    :return: None.
    """
    n0 = Node(0)
    n1 = Node(1)
    n2 = Node(2)
    e0 = Edge(n0, n1, EdgeType.UNDIRECTED)
    e1 = Edge(n1, n2, EdgeType.UNDIRECTED)

    g = Graph()
    g.add_node(n0)
    g.add_node(n1)
    g.add_edge(e0)
    g.add_edge(e1)

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


@with_setup(setup, teardown)
def test_graph_neighbor_tracking():
    """
    Tests tracking neighbors for generic graph.
    :return: None.
    """
    n0 = Node(0)
    n1 = Node(1)
    n2 = Node(2)
    e0 = Edge(n0, n1, EdgeType.UNDIRECTED)
    e1 = Edge(n1, n2, EdgeType.UNDIRECTED)

    g = Graph()
    g.add_node(n0)
    g.add_node(n1)
    g.add_edge(e0)
    g.add_edge(e1)

    assert 3 == len(g.neighbors)
    assert 1 == len(g.neighbors[0])
    assert 2 == len(g.neighbors[1])
    assert 1 == len(g.neighbors[2])
    assert 1 in g.neighbors[0]
    assert 0 in g.neighbors[1]
    assert 2 in g.neighbors[1]
    assert 1 in g.neighbors[2]

    g.remove_node(0)

    assert 0 not in g.neighbors
    assert 2 == len(g.neighbors)
    assert 1 == len(g.neighbors[1])
    assert 1 == len(g.neighbors[2])
    assert 2 in g.neighbors[1]
    assert 1 in g.neighbors[2]


@with_setup(setup, teardown)
def test_ug_neighbor_tracking():
    """
    Tests tracking neighbors for undirected graph.
    :return: None.
    """
    n0 = Node(0)
    n1 = Node(1)
    n2 = Node(2)
    e0 = Edge(n0, n1, EdgeType.UNDIRECTED)
    e1 = Edge(n1, n2, EdgeType.UNDIRECTED)

    g = Ug()
    g.add_node(n0)
    g.add_node(n1)
    g.add_edge(e0)
    g.add_edge(e1)

    assert 3 == len(g.neighbors)
    assert 1 == len(g.neighbors[0])
    assert 2 == len(g.neighbors[1])
    assert 1 == len(g.neighbors[2])
    assert 1 in g.neighbors[0]
    assert 0 in g.neighbors[1]
    assert 2 in g.neighbors[1]
    assert 1 in g.neighbors[2]

    g.remove_node(0)

    assert 0 not in g.neighbors
    assert 2 == len(g.neighbors)
    assert 1 == len(g.neighbors[1])
    assert 1 == len(g.neighbors[2])
    assert 2 in g.neighbors[1]
    assert 1 in g.neighbors[2]


@with_setup(setup, teardown)
def test_dag_neighbor_tracking():
    """
    Tests tracking neighbors for generic graph.
    :return: None.
    """
    n0 = Node(0)
    n1 = Node(1)
    n2 = Node(2)
    e0 = Edge(n0, n1, EdgeType.DIRECTED)
    e1 = Edge(n1, n2, EdgeType.DIRECTED)

    g = Dag()
    g.add_node(n0)
    g.add_node(n1)
    g.add_edge(e0)
    g.add_edge(e1)

    assert 3 == len(g.neighbors)
    assert 1 == len(g.neighbors[0])
    assert 2 == len(g.neighbors[1])
    assert 1 == len(g.neighbors[2])
    assert 1 in g.neighbors[0]
    assert 0 in g.neighbors[1]
    assert 2 in g.neighbors[1]
    assert 1 in g.neighbors[2]

    g.remove_node(0)

    assert 0 not in g.neighbors
    assert 2 == len(g.neighbors)
    assert 1 == len(g.neighbors[1])
    assert 1 == len(g.neighbors[2])
    assert 2 in g.neighbors[1]
    assert 1 in g.neighbors[2]


@with_setup(setup, teardown)
def test_copy():
    """
    Tests copy graph.
    :return: None.
    """
    n0 = Node(0)
    n1 = Node(1)
    e = Edge(n0, n1, EdgeType.UNDIRECTED)
    lhs = Graph().add_node(n0).add_node(n1).add_edge(e)
    rhs = copy.copy(lhs)

    assert len(lhs.get_nodes()) == len(rhs.get_nodes())
    for i in map(lambda n: n.id, lhs.get_nodes()):
        assert i in list(map(lambda n: n.id, rhs.get_nodes()))
    assert len(lhs.get_edges()) == len(rhs.get_edges())
    for e in map(lambda e: e.key, lhs.get_edges()):
        assert e in list(map(lambda e: e.key, rhs.get_edges()))

    lhs.get_node(0).id = 3
    assert lhs.get_node(0).id == rhs.get_node(0).id


@with_setup(setup, teardown)
def test_deepcopy():
    """
    Tests deep copy graph.
    :return: None.
    """
    n0 = Node(0)
    n1 = Node(1)
    e = Edge(n0, n1, EdgeType.UNDIRECTED)
    lhs = Graph().add_node(n0).add_node(n1).add_edge(e)
    rhs = copy.deepcopy(lhs)

    assert len(lhs.get_nodes()) == len(rhs.get_nodes())
    for i in map(lambda n: n.id, lhs.get_nodes()):
        assert i in list(map(lambda n: n.id, rhs.get_nodes()))
    assert len(lhs.get_edges()) == len(rhs.get_edges())
    for e in map(lambda e: e.key, lhs.get_edges()):
        assert e in list(map(lambda e: e.key, rhs.get_edges()))

    lhs.get_node(0).id = 3
    assert lhs.get_node(0).id != rhs.get_node(0).id
