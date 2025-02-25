import unittest

from pybbn.graph.dag import BbnUtil
from pybbn.pptc.moralizer import Moralizer
from pybbn.pptc.potentialinitializer import PotentialInitializer
from pybbn.pptc.triangulator import Triangulator


class TestTriangulator(unittest.TestCase):
    def setUp(self):
        """
        Setup.
        :return: None.
        """
        pass

    def tearDown(self):
        """
        Teardown.
        :return: None.
        """
        pass

    def test_triangulator(self):
        """
        Tests triangulation.
        :return: None.
        """
        bbn = BbnUtil.get_huang_graph()
        PotentialInitializer.init(bbn)

        ug = Moralizer.moralize(bbn)
        cliques = Triangulator.triangulate(ug)

        e_cliques = set(
            ["(d,e,f)", "(e,g,h)", "(c,e,g)", "(a,b,c)", "(b,c,d)", "(c,d,e)"]
        )

        o_cliques = [str(c) for c in cliques]

        assert len(e_cliques) == len(o_cliques)
        for c in e_cliques:
            assert c in o_cliques
