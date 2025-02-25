import unittest

from pybbn.generator.bbngenerator import (
    convert_for_drawing,
    convert_for_exact_inference,
    generate_multi_bbn,
    generate_singly_bbn,
)


class TestBbnGenerator(unittest.TestCase):
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

    def test_singly_connected(self):
        """
        Tests generating singly-connected BBN.
        :return: None.
        """
        g, p = generate_singly_bbn(3)

        assert len(g.nodes) == 3
        assert len(g.edges) == 2

    def test_multi_connected(self):
        """
        Tests generating multi-connected BBN.
        :return: None.
        """
        g, p = generate_multi_bbn(4)

        assert len(g.nodes) == 4
        assert len(g.edges) > 1

    def test_convert_for_exact_inference(self):
        """
        Tests converting graph and params to a BBN.
        :return: None
        """

        g, p = generate_singly_bbn(2)
        bbn = convert_for_exact_inference(g, p)

        assert len(bbn.nodes) == 2
        assert len(bbn.edges) == 1

    def test_convert_for_drawing(self):
        """
        Tests converting BBN to networkx DAG.
        :return: None
        """

        g, p = generate_singly_bbn(2)
        bbn = convert_for_exact_inference(g, p)

        graph = convert_for_drawing(bbn)
        nodes = list(graph.nodes)
        edges = list(graph.edges)

        assert len(nodes) == 2
        assert len(edges) == 1
