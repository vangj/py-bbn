from pybbn.graph.dag import BbnUtil
from pybbn.graph.jointree import EvidenceBuilder
from pybbn.pptc.inferencecontroller import InferenceController
from nose import with_setup


def setup():
    pass


def teardown():
    pass


@with_setup(setup, teardown)
def test_inference_controller():
    bbn = BbnUtil.get_huang_graph()
    join_tree = InferenceController.apply(bbn)

    print('INIT')
    print_potentials(join_tree)

    ev = EvidenceBuilder()\
        .with_node(join_tree.get_bbn_node(0))\
        .with_evidence('on', 1.0)\
        .build()

    join_tree.set_observation(ev)

    print('FIRST')
    print_potentials(join_tree)

    # assert 1 == 2


def print_potentials(join_tree):
    for node in join_tree.get_bbn_nodes():
        potential = join_tree.get_bbn_potential(node)
        print(node)
        print(potential)
        total = sum([entry.value for entry in potential.entries])
        print('total {}'.format(total))
        print('-----')
