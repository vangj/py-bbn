import copy
import json

from nose import with_setup
from nose.tools import assert_almost_equals

from pybbn.graph.dag import Bbn
from pybbn.graph.edge import JtEdge, Edge, EdgeType
from pybbn.graph.jointree import JoinTree
from pybbn.graph.node import BbnNode, Clique
from pybbn.graph.potential import Potential
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
    lhs = InferenceController.apply(bbn)
    rhs = copy.copy(lhs)

    assert len(lhs.get_nodes()) == len(rhs.get_nodes())
    assert len(lhs.get_edges()) == len(rhs.get_edges())
    assert len(lhs.neighbors) == len(rhs.neighbors)
    assert len(lhs.evidences) == len(rhs.evidences)
    assert len(lhs.potentials) == len(rhs.potentials)

    list(lhs.get_nodes())[0].nodes[0].variable.values[0] = 'true'
    lhs_v = list(lhs.get_nodes())[0].nodes[0].variable.values[0]
    rhs_v = list(rhs.get_nodes())[0].nodes[0].variable.values[0]
    assert lhs_v == rhs_v


@with_setup(setup, teardown)
def test_deepcopy():
    """
    Tests deep copy of join tree.
    :return: None
    """
    a = BbnNode(Variable(0, 'a', ['t', 'f']), [0.2, 0.8])
    b = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
    bbn = Bbn().add_node(a).add_node(b) \
        .add_edge(Edge(a, b, EdgeType.DIRECTED))
    lhs = InferenceController.apply(bbn)
    rhs = copy.deepcopy(lhs)

    lhs_nodes, rhs_nodes = lhs.get_nodes(), rhs.get_nodes()
    lhs_edges, rhs_edges = lhs.get_edges(), rhs.get_edges()
    lhs_neighbors, rhs_neighbors = lhs.neighbors, rhs.neighbors
    lhs_evidences, rhs_evidences = lhs.evidences, rhs.evidences
    lhs_potentials, rhs_potentials = lhs.potentials, rhs.potentials

    assert len(lhs_nodes) == len(rhs_nodes)
    assert len(lhs_edges) == len(rhs_edges)
    assert len(lhs_neighbors) == len(rhs_neighbors)
    assert len(lhs_evidences) == len(rhs_evidences)
    assert len(lhs_potentials) == len(rhs_potentials)

    list(lhs.get_nodes())[0].nodes[0].variable.values[0] = 'true'
    lhs_v = list(lhs.get_nodes())[0].nodes[0].variable.values[0]
    rhs_v = list(rhs.get_nodes())[0].nodes[0].variable.values[0]
    assert lhs_v != rhs_v


@with_setup(setup, teardown)
def test_to_dict():
    """
    Tests serializing join tree to dictionary.
    :return: None.
    """
    n0 = BbnNode(Variable(0, 'n0', ['t', 'f']), [0.2, 0.8])
    n1 = BbnNode(Variable(1, 'n1', ['t', 'f']), [0.9, 0.1, 0.9, 0.1])
    n2 = BbnNode(Variable(2, 'n2', ['t', 'f']), [0.6, 0.4, 0.4, 0.6])
    bbn = Bbn().add_node(n0).add_node(n1).add_node(n2) \
        .add_edge(Edge(n0, n1, EdgeType.DIRECTED)) \
        .add_edge(Edge(n1, n2, EdgeType.DIRECTED))
    jt = InferenceController.apply(bbn)
    d = JoinTree.to_dict(jt)
    lhs = json.dumps(d, sort_keys=True, indent=2)
    rhs = """{
  "bbn_nodes": {
    "0": {
      "probs": [
        0.2,
        0.8
      ],
      "variable": {
        "id": 0,
        "name": "n0",
        "values": [
          "t",
          "f"
        ]
      }
    },
    "1": {
      "probs": [
        0.9,
        0.1,
        0.9,
        0.1
      ],
      "variable": {
        "id": 1,
        "name": "n1",
        "values": [
          "t",
          "f"
        ]
      }
    },
    "2": {
      "probs": [
        0.6,
        0.4,
        0.4,
        0.6
      ],
      "variable": {
        "id": 2,
        "name": "n2",
        "values": [
          "t",
          "f"
        ]
      }
    }
  },
  "jt": {
    "edges": [
      "0-1-1-1-2"
    ],
    "nodes": {
      "0-1": {
        "node_ids": [
          0,
          1
        ],
        "type": "clique"
      },
      "0-1-1-1-2": {
        "left": "0-1",
        "right": "1-2",
        "type": "sepset"
      },
      "1-2": {
        "node_ids": [
          1,
          2
        ],
        "type": "clique"
      }
    },
    "parent_info": {
      "0": [],
      "1": [
        0
      ],
      "2": [
        1
      ]
    }
  }
}"""
    assert lhs == rhs


@with_setup(setup, teardown)
def test_from_dict():
    """
    Tests deserializing from dictionary.
    :return:
    """
    s = """{
  "bbn_nodes": {
    "0": {
      "probs": [
        0.2,
        0.8
      ],
      "variable": {
        "id": 0,
        "name": "n0",
        "values": [
          "t",
          "f"
        ]
      }
    },
    "1": {
      "probs": [
        0.9,
        0.1,
        0.9,
        0.1
      ],
      "variable": {
        "id": 1,
        "name": "n1",
        "values": [
          "t",
          "f"
        ]
      }
    },
    "2": {
      "probs": [
        0.6,
        0.4,
        0.4,
        0.6
      ],
      "variable": {
        "id": 2,
        "name": "n2",
        "values": [
          "t",
          "f"
        ]
      }
    }
  },
  "jt": {
    "edges": [
      "0-1-1-1-2"
    ],
    "nodes": {
      "0-1": {
        "node_ids": [
          0,
          1
        ],
        "type": "clique"
      },
      "0-1-1-1-2": {
        "left": "0-1",
        "right": "1-2",
        "type": "sepset"
      },
      "1-2": {
        "node_ids": [
          1,
          2
        ],
        "type": "clique"
      }
    },
    "parent_info": {
      "0": [],
      "1": [
        0
      ],
      "2": [
        1
      ]
    }
  }
}"""
    d = json.loads(s)
    lhs = JoinTree.from_dict(d)
    lhs = InferenceController.apply_from_serde(lhs)

    n0 = BbnNode(Variable(0, 'n0', ['t', 'f']), [0.2, 0.8])
    n1 = BbnNode(Variable(1, 'n1', ['t', 'f']), [0.9, 0.1, 0.9, 0.1])
    n2 = BbnNode(Variable(2, 'n2', ['t', 'f']), [0.6, 0.4, 0.4, 0.6])
    bbn = Bbn().add_node(n0).add_node(n1).add_node(n2) \
        .add_edge(Edge(n0, n1, EdgeType.DIRECTED)) \
        .add_edge(Edge(n1, n2, EdgeType.DIRECTED))
    rhs = InferenceController.apply(bbn)

    lhs_pot = [lhs.get_bbn_potential(n) for n in lhs.get_bbn_nodes()]
    rhs_pot = [rhs.get_bbn_potential(n) for n in rhs.get_bbn_nodes()]

    lhs_pot = Potential.to_dict(lhs_pot)
    rhs_pot = Potential.to_dict(rhs_pot)

    assert len(lhs_pot) == len(rhs_pot)

    for k, p in lhs_pot.items():
        assert_almost_equals(p, rhs_pot[k], 0.001)


@with_setup(setup, teardown)
def test_simple_serde():
    """
    Tests join tree serde with only 1 clique.
    :return: None.
    """
    a = BbnNode(Variable(0, 'a', ['t', 'f']), [0.2, 0.8])
    b = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
    bbn = Bbn().add_node(a).add_node(b) \
        .add_edge(Edge(a, b, EdgeType.DIRECTED))
    lhs = InferenceController.apply(bbn)

    d = JoinTree.to_dict(lhs)

    rhs = JoinTree.from_dict(d)
    rhs = InferenceController.apply_from_serde(rhs)

    lhs_pot = [lhs.get_bbn_potential(n) for n in lhs.get_bbn_nodes()]
    rhs_pot = [rhs.get_bbn_potential(n) for n in rhs.get_bbn_nodes()]

    lhs_pot = Potential.to_dict(lhs_pot)
    rhs_pot = Potential.to_dict(rhs_pot)

    assert len(lhs_pot) == len(rhs_pot)
