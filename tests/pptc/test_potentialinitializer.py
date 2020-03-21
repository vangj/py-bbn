from nose import with_setup

from pybbn.graph.dag import BbnUtil
from pybbn.pptc.potentialinitializer import PotentialInitializer


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
def test_potential_initializer():
    """
    Tests potential initialization.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()
    PotentialInitializer.init(bbn)

    e_potentials = {
        '0=on': 0.50000,
        '0=off': 0.50000,
        '0=on,1=on': 0.50000,
        '0=on,1=off': 0.50000,
        '0=off,1=on': 0.40000,
        '0=off,1=off': 0.60000,
        '0=on,2=on': 0.70000,
        '0=on,2=off': 0.30000,
        '0=off,2=on': 0.20000,
        '0=off,2=off': 0.80000,
        '1=on,3=on': 0.90000,
        '1=on,3=off': 0.10000,
        '1=off,3=on': 0.50000,
        '1=off,3=off': 0.50000,
        '2=on,4=on': 0.30000,
        '2=on,4=off': 0.70000,
        '2=off,4=on': 0.60000,
        '2=off,4=off': 0.40000,
        '3=on,4=on,5=on': 0.01000,
        '3=on,4=on,5=off': 0.99000,
        '3=on,4=off,5=on': 0.01000,
        '3=on,4=off,5=off': 0.99000,
        '3=off,4=on,5=on': 0.01000,
        '3=off,4=on,5=off': 0.99000,
        '3=off,4=off,5=on': 0.99000,
        '3=off,4=off,5=off': 0.01000,
        '2=on,6=on': 0.80000,
        '2=on,6=off': 0.20000,
        '2=off,6=on': 0.10000,
        '2=off,6=off': 0.90000,
        '4=on,6=on,7=on': 0.05000,
        '4=on,6=on,7=off': 0.95000,
        '4=on,6=off,7=on': 0.95000,
        '4=on,6=off,7=off': 0.05000,
        '4=off,6=on,7=on': 0.95000,
        '4=off,6=on,7=off': 0.05000,
        '4=off,6=off,7=on': 0.95000,
        '4=off,6=off,7=off': 0.05000
    }

    o_potentials = '\n'.join([str(node.potential) for node in bbn.get_nodes()]).split('\n')
    o_potentials = [p.split('|') for p in o_potentials]
    o_potentials = {tokens[0]: float(tokens[1]) for tokens in o_potentials}

    assert len(e_potentials) == len(o_potentials)
    for k, lhs in o_potentials.items():
        assert k in e_potentials
        rhs = e_potentials[k]

        assert lhs == rhs
