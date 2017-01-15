from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.node import Node
from pybbn.graph.graph import Graph
from pybbn.graph.sp.shortestpath import ShortestPath
from nose import with_setup


def setup():
    pass


def teardown():
    pass


@with_setup(setup, teardown)
def test_simple_shortest_path():
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

    assert ShortestPath(0, 1, g).exists() is True
    assert ShortestPath(0, 2, g).exists() is True
    assert ShortestPath(1, 2, g).exists() is True
    assert ShortestPath(1, 0, g).exists() is True
    assert ShortestPath(2, 1, g).exists() is True
    assert ShortestPath(2, 0, g).exists() is True
    assert ShortestPath(0, 3, g).exists() is False


