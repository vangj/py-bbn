from nose import with_setup
from nose.tools import assert_almost_equals

from pybbn.graph.dag import BbnUtil, Bbn
from pybbn.graph.edge import EdgeType, Edge
from pybbn.graph.jointree import EvidenceBuilder
from pybbn.graph.node import BbnNode
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
def test_github_issue_4():
    """
    Tests issue #4 https://github.com/vangj/py-bbn/issues/4
    :return: None.
    """
    a = BbnNode(Variable(0, 'A', ['T', 'F']), [0.5, 0.5])
    b = BbnNode(Variable(1, 'B', ['T', 'F']), [0.2, 0.8, 0.1, 0.9])
    c = BbnNode(Variable(2, 'C', ['T', 'F']), [0.5, 0.5, 0.5, 0.5])
    d = BbnNode(Variable(3, 'D', ['T', 'F']), [0.5, 0.5, 0.5, 0.5])
    e = BbnNode(Variable(4, 'E', ['T', 'F']), [0.5, 0.5, 0.5, 0.5])
    f = BbnNode(Variable(5, 'F', ['T', 'F']), [0.5, 0.5, 0.5, 0.5])
    g = BbnNode(Variable(6, 'G', ['T', 'F']),
                [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])

    bbn = Bbn() \
        .add_node(a) \
        .add_node(b) \
        .add_node(c) \
        .add_node(d) \
        .add_node(e) \
        .add_node(f) \
        .add_node(g) \
        .add_edge(Edge(a, b, EdgeType.DIRECTED)) \
        .add_edge(Edge(a, c, EdgeType.DIRECTED)) \
        .add_edge(Edge(b, d, EdgeType.DIRECTED)) \
        .add_edge(Edge(b, e, EdgeType.DIRECTED)) \
        .add_edge(Edge(c, f, EdgeType.DIRECTED)) \
        .add_edge(Edge(e, g, EdgeType.DIRECTED)) \
        .add_edge(Edge(d, g, EdgeType.DIRECTED)) \
        .add_edge(Edge(f, g, EdgeType.DIRECTED))

    join_tree = InferenceController.apply(bbn)

    expected = {
        'A': [0.5, 0.5],
        'B': [0.15, 0.85],
        'C': [0.5, 0.5],
        'D': [0.5, 0.5],
        'E': [0.5, 0.5],
        'F': [0.5, 0.5],
        'G': [0.5, 0.5]
    }

    __validate_posterior__(expected, join_tree)

    __print_potentials__(join_tree)


@with_setup(setup, teardown)
def test_inference_controller():
    """
    Tests inference controller.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()
    join_tree = InferenceController.apply(bbn)

    print('INIT')
    __print_potentials__(join_tree)

    ev = EvidenceBuilder() \
        .with_node(join_tree.get_bbn_node(0)) \
        .with_evidence('on', 1.0) \
        .build()

    join_tree.set_observation(ev)

    print('FIRST')
    __print_potentials__(join_tree)

    # assert 1 == 2


@with_setup(setup, teardown)
def test_huang_inference():
    """
    Tests inference on the Huang graph.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()

    join_tree = InferenceController.apply(bbn)

    expected = {
        'a': [0.5, 0.5],
        'b': [0.45, 0.55],
        'c': [0.45, 0.55],
        'd': [0.68, 0.32],
        'e': [0.465, 0.535],
        'f': [0.176, 0.824],
        'g': [0.415, 0.585],
        'h': [0.823, 0.177]
    }

    __validate_posterior__(expected, join_tree)

    __print_potentials__(join_tree)


@with_setup(setup, teardown)
def test_huang_inference_with_single_evidence():
    """
    Tests inference on the Huang graph with a single evidence.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()

    join_tree = InferenceController.apply(bbn)

    expected = {
        'a': [0.5, 0.5],
        'b': [0.45, 0.55],
        'c': [0.45, 0.55],
        'd': [0.68, 0.32],
        'e': [0.465, 0.535],
        'f': [0.176, 0.824],
        'g': [0.415, 0.585],
        'h': [0.823, 0.177]
    }

    __validate_posterior__(expected, join_tree)

    ev = EvidenceBuilder() \
        .with_node(join_tree.get_bbn_node_by_name('a')) \
        .with_evidence('on', 1.0) \
        .build()
    join_tree.unobserve_all()
    join_tree.set_observation(ev)

    expected = {
        'a': [1.0, 0.0],
        'b': [0.5, 0.5],
        'c': [0.7, 0.3],
        'd': [0.7, 0.3],
        'e': [0.39, 0.61],
        'f': [0.18934, 0.81066],
        'g': [0.59, 0.41],
        'h': [0.7826, 0.2174]
    }

    __validate_posterior__(expected, join_tree)


@with_setup(setup, teardown)
def test_huang_inference_with_multiple_evidence():
    """
    Tests inference on the Huang graph with a multiple evidence.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()

    join_tree = InferenceController.apply(bbn)

    expected = {
        'a': [0.5, 0.5],
        'b': [0.45, 0.55],
        'c': [0.45, 0.55],
        'd': [0.68, 0.32],
        'e': [0.465, 0.535],
        'f': [0.176, 0.824],
        'g': [0.415, 0.585],
        'h': [0.823, 0.177]
    }

    __validate_posterior__(expected, join_tree)

    ev1 = EvidenceBuilder() \
        .with_node(join_tree.get_bbn_node_by_name('a')) \
        .with_evidence('on', 1.0) \
        .build()
    ev2 = EvidenceBuilder() \
        .with_node(join_tree.get_bbn_node_by_name('f')) \
        .with_evidence('on', 1.0) \
        .build()

    join_tree.unobserve_all()
    join_tree.update_evidences([ev1, ev2])

    expected = {
        'a': [1.0, 0.0],
        'b': [0.184, 0.816],
        'c': [0.798, 0.202],
        'd': [0.0370, 0.963],
        'e': [0.0206, 0.979],
        'f': [1.0, 0.0],
        'g': [0.658, 0.342],
        'h': [0.941, 0.0588]
    }

    __validate_posterior__(expected, join_tree)


@with_setup(setup, teardown)
def test_simple_inference():
    """
    Tests inference on the Huang graph.
    :return: None.
    """
    bbn = BbnUtil.get_simple()

    join_tree = InferenceController.apply(bbn)

    expected = {
        'a': [0.5, 0.5],
        'b': [0.45, 0.55],
        'c': [0.45, 0.55],
        'd': [0.68, 0.32],
        'e': [0.465, 0.535],
        'f': [0.176, 0.824]
    }

    __validate_posterior__(expected, join_tree)

    __print_potentials__(join_tree)


@with_setup(setup, teardown)
def test_inference_1():
    """
    Tests inference on the Huang graph with manual construction.
    :return: None.
    """
    a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
    b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
    c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])
    d = BbnNode(Variable(3, 'd', ['on', 'off']), [0.9, 0.1, 0.5, 0.5])
    e = BbnNode(Variable(4, 'e', ['on', 'off']), [0.3, 0.7, 0.6, 0.4])
    f = BbnNode(Variable(5, 'f', ['on', 'off']), [0.01, 0.99, 0.01, 0.99, 0.01, 0.99, 0.99, 0.01])
    g = BbnNode(Variable(6, 'g', ['on', 'off']), [0.8, 0.2, 0.1, 0.9])
    h = BbnNode(Variable(7, 'h', ['on', 'off']), [0.05, 0.95, 0.95, 0.05, 0.95, 0.05, 0.95, 0.05])

    bbn = Bbn() \
        .add_node(a) \
        .add_node(b) \
        .add_node(c) \
        .add_node(d) \
        .add_node(e) \
        .add_node(f) \
        .add_node(g) \
        .add_node(h) \
        .add_edge(Edge(a, b, EdgeType.DIRECTED)) \
        .add_edge(Edge(a, c, EdgeType.DIRECTED)) \
        .add_edge(Edge(b, d, EdgeType.DIRECTED)) \
        .add_edge(Edge(c, e, EdgeType.DIRECTED)) \
        .add_edge(Edge(d, f, EdgeType.DIRECTED)) \
        .add_edge(Edge(e, f, EdgeType.DIRECTED)) \
        .add_edge(Edge(c, g, EdgeType.DIRECTED)) \
        .add_edge(Edge(e, h, EdgeType.DIRECTED)) \
        .add_edge(Edge(g, h, EdgeType.DIRECTED))

    join_tree = InferenceController.apply(bbn)

    expected = {
        'a': [0.5, 0.5],
        'b': [0.45, 0.55],
        'c': [0.45, 0.55],
        'd': [0.680, 0.32],
        'e': [0.465, 0.535],
        'f': [0.176, 0.824],
        'g': [0.415, 0.585],
        'h': [0.823, 0.177]
    }

    __validate_posterior__(expected, join_tree)


@with_setup(setup, teardown)
def test_inference_2():
    """
    Tests inference on customized graph.
    :return: None.
    """
    a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.7, 0.3])
    b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.4, 0.6])
    c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.9, 0.1, 0.3, 0.7, 0.5, 0.5, 0.1, 0.9])
    d = BbnNode(Variable(3, 'd', ['on', 'off']), [0.3, 0.7, 0.8, 0.2])
    e = BbnNode(Variable(4, 'e', ['on', 'off']), [0.6, 0.4, 0.2, 0.8])
    f = BbnNode(Variable(5, 'f', ['on', 'off']), [0.7, 0.3, 0.1, 0.9])
    g = BbnNode(Variable(6, 'g', ['on', 'off']), [0.4, 0.6, 0.9, 0.1])

    bbn = Bbn() \
        .add_node(a) \
        .add_node(b) \
        .add_node(c) \
        .add_node(d) \
        .add_node(e) \
        .add_node(f) \
        .add_node(g) \
        .add_edge(Edge(a, c, EdgeType.DIRECTED)) \
        .add_edge(Edge(b, c, EdgeType.DIRECTED)) \
        .add_edge(Edge(c, d, EdgeType.DIRECTED)) \
        .add_edge(Edge(c, e, EdgeType.DIRECTED)) \
        .add_edge(Edge(d, f, EdgeType.DIRECTED)) \
        .add_edge(Edge(d, g, EdgeType.DIRECTED))

    join_tree = InferenceController.apply(bbn)

    expected = {
        'a': [0.7, 0.3],
        'b': [0.4, 0.6],
        'c': [0.456, 0.544],
        'd': [0.572, 0.428],
        'e': [0.382, 0.618],
        'f': [0.443, 0.557],
        'g': [0.614, 0.386]
    }

    __validate_posterior__(expected, join_tree)


@with_setup(setup, teardown)
def test_inference_4():
    """
    Tests inference on simple customized graph.
    :return: None.
    """
    a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.7, 0.3])
    b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.4, 0.6])
    c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.9, 0.1, 0.3, 0.7, 0.5, 0.5, 0.1, 0.9])
    e = BbnNode(Variable(4, 'e', ['on', 'off']), [0.6, 0.4, 0.2, 0.8])

    bbn = Bbn() \
        .add_node(a) \
        .add_node(b) \
        .add_node(c) \
        .add_node(e) \
        .add_edge(Edge(a, c, EdgeType.DIRECTED)) \
        .add_edge(Edge(b, c, EdgeType.DIRECTED)) \
        .add_edge(Edge(c, e, EdgeType.DIRECTED))

    join_tree = InferenceController.apply(bbn)

    expected = {
        'a': [0.7, 0.3],
        'b': [0.4, 0.6],
        'c': [0.456, 0.544],
        'e': [0.3824, 0.6176]
    }

    __validate_posterior__(expected, join_tree)


@with_setup(setup, teardown)
def test_inference_libpgm():
    """
    Tests inference with evidence on libpgm graph.
    :return: None.
    """
    difficulty = BbnNode(Variable(0, 'difficulty', ['easy', 'hard']), [0.6, 0.4])
    intelligence = BbnNode(Variable(1, 'intelligence', ['low', 'high']), [0.7, 0.3])
    grade = BbnNode(Variable(2, 'grade', ['a', 'b', 'c']),
                    [0.3, 0.4, 0.3, 0.9, 0.08, 0.02, 0.05, 0.25, 0.7, 0.5, 0.3, 0.2])
    sat = BbnNode(Variable(3, 'sat', ['low', 'high']), [0.95, 0.05, 0.2, 0.8])
    letter = BbnNode(Variable(4, 'letter', ['weak', 'strong']), [0.1, 0.9, 0.4, 0.6, 0.99, 0.01])

    bbn = Bbn() \
        .add_node(difficulty) \
        .add_node(intelligence) \
        .add_node(grade) \
        .add_node(sat) \
        .add_node(letter) \
        .add_edge(Edge(difficulty, grade, EdgeType.DIRECTED)) \
        .add_edge(Edge(intelligence, grade, EdgeType.DIRECTED)) \
        .add_edge(Edge(intelligence, sat, EdgeType.DIRECTED)) \
        .add_edge(Edge(grade, letter, EdgeType.DIRECTED))

    join_tree = InferenceController.apply(bbn)

    __validate_posterior__({
        'difficulty': [0.6, 0.4],
        'intelligence': [0.7, 0.3],
        'grade': [0.362, 0.288, 0.350],
        'sat': [0.725, 0.275],
        'letter': [0.498, 0.502]
    }, join_tree)

    ev = EvidenceBuilder() \
        .with_node(join_tree.get_bbn_node_by_name('sat')) \
        .with_evidence('high', 1.0) \
        .build()
    join_tree.unobserve_all()
    join_tree.set_observation(ev)

    __validate_posterior__({
        'difficulty': [0.6, 0.4],
        'intelligence': [0.127, 0.873],
        'grade': [0.671, 0.190, 0.139],
        'sat': [0.0, 1.0],
        'letter': [0.281, 0.719]
    }, join_tree)

    ev = EvidenceBuilder() \
        .with_node(join_tree.get_bbn_node_by_name('sat')) \
        .with_evidence('low', 1.0) \
        .build()
    join_tree.unobserve_all()
    join_tree.set_observation(ev)

    __validate_posterior__({
        'difficulty': [0.6, 0.4],
        'intelligence': [0.917, 0.0828],
        'grade': [0.245, 0.326, 0.430],
        'sat': [1.0, 0.0],
        'letter': [0.58, 0.42]
    }, join_tree)


@with_setup(setup, teardown)
def test_inference_libpgm2():
    """
    Tests libpgm graph where ordering messes up computation.
    :return: None.
    """
    letter = BbnNode(
        Variable(4, 'Letter', ['weak', 'strong']),
        [0.1, 0.9, 0.4, 0.6, 0.99, 0.01])
    grade = BbnNode(
        Variable(2, 'Grade', ['a', 'b', 'c']),
        [0.3, 0.4, 0.3, 0.9, 0.08, 0.02, 0.05, 0.25, 0.7, 0.5, 0.3, 0.2])
    intelligence = BbnNode(
        Variable(3, 'Intelligence', ['low', 'high']),
        [0.7, 0.3])
    sat = BbnNode(
        Variable(1, 'SAT', ['low', 'high']),
        [0.95, 0.05, 0.2, 0.8])
    difficulty = BbnNode(
        Variable(0, 'Difficulty', ['easy', 'hard']),
        [0.6, 0.4])

    bbn = Bbn() \
        .add_node(letter) \
        .add_node(grade) \
        .add_node(intelligence) \
        .add_node(sat) \
        .add_node(difficulty) \
        .add_edge(Edge(difficulty, grade, EdgeType.DIRECTED)) \
        .add_edge(Edge(intelligence, grade, EdgeType.DIRECTED)) \
        .add_edge(Edge(intelligence, sat, EdgeType.DIRECTED)) \
        .add_edge(Edge(grade, letter, EdgeType.DIRECTED))

    join_tree = InferenceController.apply(bbn)

    __validate_posterior__({
        'Difficulty': [0.6, 0.4],
        'Intelligence': [0.7, 0.3],
        'Grade': [0.362, 0.288, 0.350],
        'SAT': [0.725, 0.275],
        'Letter': [0.498, 0.502]
    }, join_tree, debug=False)


@with_setup(setup, teardown)
def test_trivial_inference():
    """
    Tests inference on trivial graphs.
    :return: None.
    """
    a1 = BbnNode(Variable(0, 'a', ['t', 'f']), [0.2, 0.8])
    b1 = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
    bbn1 = Bbn().add_node(a1).add_node(b1).add_edge(Edge(a1, b1, EdgeType.DIRECTED))
    jt1 = InferenceController.apply(bbn1)

    a2 = BbnNode(Variable(1, 'a', ['t', 'f']), [0.2, 0.8])
    b2 = BbnNode(Variable(0, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
    bbn2 = Bbn().add_node(a2).add_node(b2).add_edge(Edge(a2, b2, EdgeType.DIRECTED))
    jt2 = InferenceController.apply(bbn2)

    a3 = BbnNode(Variable(0, 'a', ['t', 'f']), [0.2, 0.8])
    b3 = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9])
    bbn3 = Bbn().add_node(a3).add_node(b3)
    jt3 = InferenceController.apply(bbn3)

    __validate_posterior__({
        'a': [0.2, 0.8],
        'b': [0.74, 0.26]
    }, jt1, debug=False)

    __validate_posterior__({
        'a': [0.2, 0.8],
        'b': [0.74, 0.26]
    }, jt2, debug=False)

    __validate_posterior__({
        'a': [0.2, 0.8],
        'b': [0.1, 0.9]
    }, jt3, debug=False)


@with_setup(setup, teardown)
def test_inference_var_permutation():
    """
    Tests inference on graphs where id are reversed.
    :return: None.
    """
    a1 = BbnNode(Variable(0, 'a', ['t', 'f']), [0.2, 0.8])
    b1 = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
    c1 = BbnNode(Variable(2, 'c', ['t', 'f']), [0.2, 0.8, 0.7, 0.3])
    bbn1 = Bbn().add_node(a1).add_node(b1).add_node(c1) \
        .add_edge(Edge(a1, b1, EdgeType.DIRECTED)) \
        .add_edge(Edge(b1, c1, EdgeType.DIRECTED))
    jt1 = InferenceController.apply(bbn1)

    a2 = BbnNode(Variable(2, 'a', ['t', 'f']), [0.2, 0.8])
    b2 = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
    c2 = BbnNode(Variable(0, 'c', ['t', 'f']), [0.2, 0.8, 0.7, 0.3])
    bbn2 = Bbn().add_node(a2).add_node(b2).add_node(c2) \
        .add_edge(Edge(a2, b2, EdgeType.DIRECTED)) \
        .add_edge(Edge(b2, c2, EdgeType.DIRECTED))
    jt2 = InferenceController.apply(bbn2)

    __validate_posterior__({
        'a': [0.2, 0.8],
        'b': [0.74, 0.26],
        'c': [0.33, 0.67]
    }, jt1, debug=False)

    __validate_posterior__({
        'a': [0.2, 0.8],
        'b': [0.74, 0.26],
        'c': [0.33, 0.67]
    }, jt2, debug=False)


@with_setup(setup, teardown)
def test_forest_inference():
    """
    Tests inference on a disconnected DAG; sub-DAGs are a -> b, c -> d and e -> f.
    :return: None.
    """
    a = BbnNode(Variable(0, 'a', ['t', 'f']), [0.2, 0.8])
    b = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
    c = BbnNode(Variable(2, 'c', ['t', 'f']), [0.2, 0.8])
    d = BbnNode(Variable(3, 'd', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
    e = BbnNode(Variable(4, 'e', ['t', 'f']), [0.2, 0.8])
    f = BbnNode(Variable(5, 'f', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
    bbn = Bbn().add_node(a).add_node(b).add_node(c).add_node(d).add_node(e).add_node(f) \
        .add_edge(Edge(a, b, EdgeType.DIRECTED)) \
        .add_edge(Edge(c, d, EdgeType.DIRECTED)) \
        .add_edge(Edge(e, f, EdgeType.DIRECTED))

    jt = InferenceController.apply(bbn)
    pot = [jt.get_bbn_potential(n) for n in jt.get_bbn_nodes()]
    o = Potential.to_dict(pot)
    e = {
        '0=t': 0.2,
        '0=f': 0.8,
        '1=t': 0.7400000000000001,
        '1=f': 0.26,
        '2=t': 0.2,
        '2=f': 0.8,
        '3=t': 0.7400000000000001,
        '3=f': 0.26,
        '4=t': 0.2,
        '4=f': 0.8,
        '5=t': 0.7400000000000001,
        '5=f': 0.26
    }

    for k, p in e.items():
        assert_almost_equals(p, o[k], 0.001)


@with_setup(setup, teardown)
def test_reapply():
    """
    Tests reinitializing join tree after updating CPTs.
    :return: None.
    """
    a = BbnNode(Variable(0, 'a', ['t', 'f']), [0.2, 0.8])
    b = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
    bbn = Bbn().add_node(a).add_node(b) \
        .add_edge(Edge(a, b, EdgeType.DIRECTED))

    lhs = InferenceController.apply(bbn)
    rhs = InferenceController.reapply(lhs, {0: [0.3, 0.7], 1: [0.2, 0.8, 0.8, 0.2]})

    lhs_pot = [lhs.get_bbn_potential(n) for n in lhs.get_bbn_nodes()]
    rhs_pot = [rhs.get_bbn_potential(n) for n in rhs.get_bbn_nodes()]

    lhs_d = Potential.to_dict(lhs_pot)
    rhs_d = Potential.to_dict(rhs_pot)

    # lhs should not match rhs after CPT update
    for k, prob in lhs_d.items():
        assert k in rhs_d
        assert prob != rhs_d[k]

    # now create lhs with same params as param used to update old
    # should match with rhs since params are now the same
    a = BbnNode(Variable(0, 'a', ['t', 'f']), [0.3, 0.7])
    b = BbnNode(Variable(1, 'b', ['t', 'f']), [0.2, 0.8, 0.8, 0.2])
    bbn = Bbn().add_node(a).add_node(b) \
        .add_edge(Edge(a, b, EdgeType.DIRECTED))

    lhs = InferenceController.apply(bbn)
    lhs_pot = [lhs.get_bbn_potential(n) for n in lhs.get_bbn_nodes()]
    lhs_d = Potential.to_dict(lhs_pot)

    for k, prob in lhs_d.items():
        assert k in rhs_d
        assert_almost_equals(prob, rhs_d[k], 0.001)


def __validate_posterior__(expected, join_tree, debug=False):
    """
    Validates the posterior probabilities of a join tree.
    :param expected: Expected posteriors.
    :param join_tree: Join tree.
    :param debug: Flag indicating if we should debug.
    :return: None.
    """
    for node in join_tree.get_bbn_nodes():
        potential = join_tree.get_bbn_potential(node)
        if debug is True:
            p = ', '.join(['{}'.format(e) for e in potential.entries])
            s = '{} : {}'.format(node.variable.name, p)
            print(s)

        o = [e.value for e in potential.entries]
        e = expected[node.variable.name]

        assert len(o) == len(e)
        for ob, ex in zip(o, e):
            diff = abs(ob - ex)
            if diff > 0.001 and debug:
                print('\t**observed={}, expected={}'.format(ob, ex))
            elif debug is False:
                assert diff < 0.001


def __print_potentials__(join_tree):
    """
    Prints the potentials.
    :param join_tree: Join tree.
    :return: None.
    """
    for node in join_tree.get_bbn_nodes():
        potential = join_tree.get_bbn_potential(node)
        p = ', '.join([f'{e}' for e in potential.entries])
        s = f'{node.variable.name} : {p}'
        total = sum([entry.value for entry in potential.entries])
        print(f'{s} ==> {total:.5f}')
