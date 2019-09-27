from nose import with_setup

from pybbn.graph.dag import Bbn
from pybbn.graph.edge import JtEdge, Edge, EdgeType
from pybbn.graph.jointree import JoinTree
from pybbn.graph.node import BbnNode, Clique
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController


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
def test_jointree_creation():
    """
    Tests join tree creation.
    :return: None.
    """
    n0 = BbnNode(Variable(0, 'n0', ['t', 'f']), [])
    n1 = BbnNode(Variable(1, 'n1', ['t', 'f']), [])
    n2 = BbnNode(Variable(2, 'n2', ['t', 'f']), [])

    clique0 = Clique([n0, n1])
    clique1 = Clique([n1, n2])
    sep_set0 = clique0.get_sep_set(clique1)
    sep_set1 = clique0.get_sep_set(clique1)
    sep_set2 = clique1.get_sep_set(clique0)
    sep_set3 = clique0.get_sep_set(clique0)

    e0 = JtEdge(sep_set0)
    e1 = JtEdge(sep_set1)
    e2 = JtEdge(sep_set2)
    e3 = JtEdge(sep_set3)

    g = JoinTree().add_edge(e0).add_edge(e1).add_edge(e2).add_edge(e3)

    nodes = g.get_nodes()
    edges = g.get_edges()

    assert len(nodes) == 3
    assert len(edges) == 1
    assert len(g.get_flattened_edges()) == 2


@with_setup(setup, teardown)
def test_copy():
    """
    Tests copy of join tree.
    :return: None
    """
    a = BbnNode(Variable(0, 'a', ['t', 'f']), [0.2, 0.8])
    b = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
    bbn = Bbn().add_node(a).add_node(b) \
        .add_edge(Edge(a, b, EdgeType.DIRECTED))
    o = InferenceController.apply(bbn)

    print(o)
