from nose import with_setup

from pybbn.graph.dag import BbnUtil
from pybbn.graph.jointree import EvidenceBuilder
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
def test_inference_controller():
    """
    Tests inference controller.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()
    join_tree = InferenceController.apply(bbn)

    print('INIT')
    print_potentials(join_tree)

    ev = EvidenceBuilder() \
        .with_node(join_tree.get_bbn_node(0)) \
        .with_evidence('on', 1.0) \
        .build()

    join_tree.set_observation(ev)

    print('FIRST')
    print_potentials(join_tree)

    # assert 1 == 2


def print_potentials(join_tree):
    """
    Prints the potentials.
    :param join_tree: Join tree.
    :return: None.
    """
    for node in join_tree.get_bbn_nodes():
        potential = join_tree.get_bbn_potential(node)
        print(node)
        print(potential)
        total = sum([entry.value for entry in potential.entries])
        print('total {}'.format(total))
        print('-----')
