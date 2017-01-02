from pybbn.graph.edge import Edge
from pybbn.graph.node import Node
from pybbn.graph.graph import Graph
from nose import with_setup


def setup():
    pass


def teardown():
    pass


@with_setup(setup, teardown)
def test_graph_creation():
    n0 = Node(0)
    n1 = Node(1)
    n2 = Node(2)
    e0 = Edge(n0, n1)
    e1 = Edge(n1, n2)

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

    assert n1 in g.get_neighbors(0)
    assert n0 in g.get_neighbors(1)
    assert n2 in g.get_neighbors(1)
    assert n1 in g.get_neighbors(2)

