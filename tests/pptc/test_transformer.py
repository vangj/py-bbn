from pybbn.graph.dag import BbnUtil
from pybbn.pptc.potentialinitializer import PotentialInitializer
from pybbn.pptc.moralizer import Moralizer
from pybbn.pptc.triangulator import Triangulator
from pybbn.pptc.transformer import Transformer
from nose import with_setup


def setup():
    pass


def teardown():
    pass


@with_setup(setup, teardown)
def test_transformer():
    bbn = BbnUtil.get_huang_graph()
    PotentialInitializer.init(bbn)

    ug = Moralizer.moralize(bbn)
    cliques = Triangulator.triangulate(ug)

    join_tree = Transformer.transform(cliques)

    # assert later
    # print(join_tree)
    # assert 1 == 2
