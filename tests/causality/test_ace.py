from nose import with_setup

from pybbn.causality.ace import Ace
from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable


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


def get_drug_network():
    gender_probs = [0.49, 0.51]
    drug_probs = [0.23323615160349853, 0.7667638483965015,
                  0.7563025210084033, 0.24369747899159663]
    recovery_probs = [0.31000000000000005, 0.69,
                      0.27, 0.73,
                      0.13, 0.87,
                      0.06999999999999995, 0.93]

    X = BbnNode(Variable(1, 'drug', ['false', 'true']), drug_probs)
    Y = BbnNode(Variable(2, 'recovery', ['false', 'true']), recovery_probs)
    Z = BbnNode(Variable(0, 'gender', ['female', 'male']), gender_probs)

    bbn = Bbn() \
        .add_node(X) \
        .add_node(Y) \
        .add_node(Z) \
        .add_edge(Edge(Z, X, EdgeType.DIRECTED)) \
        .add_edge(Edge(Z, Y, EdgeType.DIRECTED)) \
        .add_edge(Edge(X, Y, EdgeType.DIRECTED))

    return bbn


@with_setup(setup, teardown)
def test_ace():
    """
    Tests getting average causal effect.
    """
    bbn = get_drug_network()
    ace = Ace(bbn)
    results = ace.get_ace('drug', 'recovery', 'true')
    t = results['true']
    f = results['false']

    assert t - 0.832 < 0.001
    assert f - 0.782 < 0.001
