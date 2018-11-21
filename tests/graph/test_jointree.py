from nose import with_setup

from pybbn.graph.dag import Bbn, BbnUtil
from pybbn.graph.edge import JtEdge, Edge, EdgeType
from pybbn.graph.jointree import JoinTree, EvidenceBuilder
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
def test_huang_inference():
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


@with_setup(setup, teardown)
def test_inference_1():
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
        .add_edge(Edge(c, e, EdgeType.DIRECTED)) \

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
    # letter = BbnNode(
    #     Variable(0, 'letter', ['weak', 'strong']),
    #     [0.1, 0.9, 0.4, 0.6, 0.99, 0.01])
    # grade = BbnNode(
    #     Variable(1, 'grade', ['a', 'b', 'c']),
    #     [0.3, 0.4, 0.3, 0.9, 0.08, 0.02, 0.05, 0.25, 0.7, 0.5, 0.3, 0.2])
    # intelligence = BbnNode(
    #     Variable(2, 'intelligence', ['low', 'high']),
    #     [0.7, 0.3])
    # sat = BbnNode(
    #     Variable(3, 'sat', ['low', 'high']),
    #     [0.95, 0.05, 0.2, 0.8])
    # difficulty = BbnNode(
    #     Variable(4, 'difficulty', ['easy', 'hard']),
    #     [0.6, 0.4])

    letter = BbnNode(
        Variable(2, 'Letter', ['weak', 'strong']),
        [0.1, 0.9, 0.4, 0.6, 0.99, 0.01])
    grade = BbnNode(
        Variable(4, 'Grade', ['a', 'b', 'c']),
        [0.3, 0.4, 0.3, 0.9, 0.08, 0.02, 0.05, 0.25, 0.7, 0.5, 0.3, 0.2])
    intelligence = BbnNode(
        Variable(1, 'Intelligence', ['low', 'high']),
        [0.7, 0.3])
    sat = BbnNode(
        Variable(0, 'SAT', ['low', 'high']),
        [0.95, 0.05, 0.2, 0.8])
    difficulty = BbnNode(
        Variable(3, 'Difficulty', ['easy', 'hard']),
        [0.6, 0.4])

    bbn = Bbn() \
        .add_node(grade) \
        .add_node(intelligence) \
        .add_node(difficulty) \
        .add_node(letter) \
        .add_node(sat) \
        .add_edge(Edge(difficulty, grade, EdgeType.DIRECTED)) \
        .add_edge(Edge(intelligence, grade, EdgeType.DIRECTED)) \
        .add_edge(Edge(grade, letter, EdgeType.DIRECTED)) \
        .add_edge(Edge(intelligence, sat, EdgeType.DIRECTED))

    join_tree = InferenceController.apply(bbn)

    __validate_posterior__({
        'Difficulty': [0.6, 0.4],
        'Intelligence': [0.7, 0.3],
        'Grade': [0.362, 0.288, 0.350],
        'SAT': [0.725, 0.275],
        'Letter': [0.498, 0.502]
    }, join_tree, debug=True)


def __validate_posterior__(expected, join_tree, debug=False):
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
