from nose import with_setup

from pybbn.graph.dag import BbnUtil
from pybbn.pptc.initializer import Initializer
from pybbn.pptc.moralizer import Moralizer
from pybbn.pptc.potentialinitializer import PotentialInitializer
from pybbn.pptc.propagator import Propagator
from pybbn.pptc.transformer import Transformer
from pybbn.pptc.triangulator import Triangulator


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
def test_propagator():
    """
    Tests propagation.
    :return: None.
    """
    bbn = BbnUtil.get_huang_graph()
    PotentialInitializer.init(bbn)

    ug = Moralizer.moralize(bbn)
    cliques = Triangulator.triangulate(ug)

    join_tree = Transformer.transform(cliques)

    Initializer.initialize(join_tree)
    Propagator.propagate(join_tree)

    e_potentials = {
        '3=on,4=on,5=on': 0.00315,
        '3=on,4=on,5=off': 0.31155,
        '3=on,4=off,5=on': 0.00365,
        '3=on,4=off,5=off': 0.36165,
        '3=off,4=on,5=on': 0.00150,
        '3=off,4=on,5=off': 0.14880,
        '3=off,4=off,5=on': 0.16800,
        '3=off,4=off,5=off': 0.00170,
        '4=on,6=on,7=on': 0.00705,
        '4=on,6=on,7=off': 0.13395,
        '4=on,6=off,7=on': 0.30780,
        '4=on,6=off,7=off': 0.01620,
        '4=off,6=on,7=on': 0.26030,
        '4=off,6=on,7=off': 0.01370,
        '4=off,6=off,7=on': 0.24795,
        '4=off,6=off,7=off': 0.01305,
        '2=on,4=on,6=on': 0.10800,
        '2=on,4=on,6=off': 0.02700,
        '2=on,4=off,6=on': 0.25200,
        '2=on,4=off,6=off': 0.06300,
        '2=off,4=on,6=on': 0.03300,
        '2=off,4=on,6=off': 0.29700,
        '2=off,4=off,6=on': 0.02200,
        '2=off,4=off,6=off': 0.19800,
        '0=on,1=on,2=on': 0.17500,
        '0=off,1=on,2=on': 0.04000,
        '0=on,1=on,2=off': 0.07500,
        '0=off,1=on,2=off': 0.16000,
        '0=on,1=off,2=on': 0.17500,
        '0=off,1=off,2=on': 0.06000,
        '0=on,1=off,2=off': 0.07500,
        '0=off,1=off,2=off': 0.24000,
        '1=on,2=on,3=on': 0.19350,
        '1=off,2=on,3=on': 0.11750,
        '1=on,2=on,3=off': 0.02150,
        '1=off,2=on,3=off': 0.11750,
        '1=on,2=off,3=on': 0.21150,
        '1=off,2=off,3=on': 0.15750,
        '1=on,2=off,3=off': 0.02350,
        '1=off,2=off,3=off': 0.15750,
        '2=on,3=on,4=on': 0.09330,
        '2=off,3=on,4=on': 0.22140,
        '2=on,3=on,4=off': 0.21770,
        '2=off,3=on,4=off': 0.14760,
        '2=on,3=off,4=on': 0.04170,
        '2=off,3=off,4=on': 0.10860,
        '2=on,3=off,4=off': 0.09730,
        '2=off,3=off,4=off': 0.07240,
        '1=on,2=on': 0.21500,
        '1=on,2=off': 0.23500,
        '1=off,2=on': 0.23500,
        '1=off,2=off': 0.31500,
        '2=on,3=on': 0.31100,
        '2=on,3=off': 0.13900,
        '2=off,3=on': 0.36900,
        '2=off,3=off': 0.18100,
        '2=on,4=on': 0.13500,
        '2=on,4=off': 0.31500,
        '2=off,4=on': 0.33000,
        '2=off,4=off': 0.22000,
        '3=on,4=on': 0.31470,
        '3=on,4=off': 0.36530,
        '3=off,4=on': 0.15030,
        '3=off,4=off': 0.16970,
        '4=on,6=on': 0.14100,
        '4=on,6=off': 0.32400,
        '4=off,6=on': 0.27400,
        '4=off,6=off': 0.26100
    }

    o_potentials = '\n'.join([str(v) for _, v in join_tree.potentials.items()]).split('\n')
    o_potentials = [p.split('|') for p in o_potentials]
    o_potentials = {tokens[0]: float(tokens[1]) for tokens in o_potentials}

    assert len(e_potentials) == len(o_potentials)
    for k, lhs in o_potentials.items():
        assert k in e_potentials
        rhs = e_potentials[k]

        assert lhs == rhs
