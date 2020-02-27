import json

import numpy as np
from nose import with_setup

from pybbn.generator.bbngenerator import generate_singly_bbn, convert_for_exact_inference
from pybbn.graph.dag import Dag, BbnUtil, Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.node import Node


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


@with_setup(setup, teardown)
def test_csv_serde():
    """
    Tests CSV serde.
    :return: None.
    """
    try:
        lhs = BbnUtil.get_huang_graph()
        Bbn.to_csv(lhs, 'huang.csv')

        rhs = Bbn.from_csv('huang.csv')

        assert len(lhs.get_nodes()) == len(rhs.get_nodes())
        assert len(lhs.get_edges()) == len(rhs.get_edges())

        lhs_nodes = set([str(node) for node in lhs.get_nodes()])
        rhs_nodes = set([str(node) for node in rhs.get_nodes()])
        for n in lhs_nodes:
            assert n in rhs_nodes

        lhs_edges = set([str(edge) for edge in lhs.get_edges()])
        rhs_edges = set([str(edge) for edge in rhs.get_edges()])
        for e in lhs_edges:
            assert e in rhs_edges
    except:
        assert False
    finally:
        import os

        try:
            os.remove('huang.csv')
        except:
            pass


@with_setup(setup, teardown)
def test_to_dict():
    """
    Tests creating serializable dictionary representation.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()
    d = Bbn.to_dict(bbn)
    j = json.dumps(d, sort_keys=True, indent=2)
    e = """{
  "edges": [
    {
      "ch": 1,
      "pa": 0
    },
    {
      "ch": 2,
      "pa": 0
    },
    {
      "ch": 3,
      "pa": 1
    },
    {
      "ch": 4,
      "pa": 2
    },
    {
      "ch": 5,
      "pa": 3
    },
    {
      "ch": 5,
      "pa": 4
    },
    {
      "ch": 6,
      "pa": 2
    },
    {
      "ch": 7,
      "pa": 4
    },
    {
      "ch": 7,
      "pa": 6
    }
  ],
  "nodes": {
    "0": {
      "probs": [
        0.5,
        0.5
      ],
      "variable": {
        "id": 0,
        "name": "a",
        "values": [
          "on",
          "off"
        ]
      }
    },
    "1": {
      "probs": [
        0.5,
        0.5,
        0.4,
        0.6
      ],
      "variable": {
        "id": 1,
        "name": "b",
        "values": [
          "on",
          "off"
        ]
      }
    },
    "2": {
      "probs": [
        0.7,
        0.3,
        0.2,
        0.8
      ],
      "variable": {
        "id": 2,
        "name": "c",
        "values": [
          "on",
          "off"
        ]
      }
    },
    "3": {
      "probs": [
        0.9,
        0.1,
        0.5,
        0.5
      ],
      "variable": {
        "id": 3,
        "name": "d",
        "values": [
          "on",
          "off"
        ]
      }
    },
    "4": {
      "probs": [
        0.3,
        0.7,
        0.6,
        0.4
      ],
      "variable": {
        "id": 4,
        "name": "e",
        "values": [
          "on",
          "off"
        ]
      }
    },
    "5": {
      "probs": [
        0.01,
        0.99,
        0.01,
        0.99,
        0.01,
        0.99,
        0.99,
        0.01
      ],
      "variable": {
        "id": 5,
        "name": "f",
        "values": [
          "on",
          "off"
        ]
      }
    },
    "6": {
      "probs": [
        0.8,
        0.2,
        0.1,
        0.9
      ],
      "variable": {
        "id": 6,
        "name": "g",
        "values": [
          "on",
          "off"
        ]
      }
    },
    "7": {
      "probs": [
        0.05,
        0.95,
        0.95,
        0.05,
        0.95,
        0.05,
        0.95,
        0.05
      ],
      "variable": {
        "id": 7,
        "name": "h",
        "values": [
          "on",
          "off"
        ]
      }
    }
  }
}"""

    assert len(j) == len(e)
    assert j == e


@with_setup(setup, teardown)
def test_generated_serde():
    """
    Tests serde of generated BBN.
    :return: Nonde.
    """
    g, p = generate_singly_bbn(100, max_iter=10)
    e_bbn = convert_for_exact_inference(g, p)
    d = Bbn.to_dict(e_bbn)
    s = json.dumps(d, sort_keys=True, indent=2)
    d = json.loads(s)
    o_bbn = Bbn.from_dict(d)

    assert len(e_bbn.get_nodes()) == len(o_bbn.get_nodes())
    assert len(e_bbn.get_edges()) == len(o_bbn.get_edges())


@with_setup(setup, teardown)
def test_from_dict():
    """
    Tests creating BBN from dictionary (deserialized from JSON).
    :return: None.
    """
    e_bbn = BbnUtil.get_huang_graph()
    o_bbn = Bbn.from_dict(Bbn.to_dict(e_bbn))

    assert len(e_bbn.get_nodes()) == len(o_bbn.get_nodes())
    assert len(e_bbn.get_edges()) == len(o_bbn.get_edges())
