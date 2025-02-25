import copy
import unittest

from pybbn.graph.edge import Edge, EdgeType


class TestEdge(unittest.TestCase):
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

    def test_copy(self):
        """
        Tests edge copy.
        :return: None.
        """
        lhs = Edge(0, 1, EdgeType.UNDIRECTED)
        rhs = copy.copy(lhs)

        assert lhs.i == rhs.i
        assert lhs.j == rhs.j
        assert lhs.type == rhs.type

    def test_deepcopy(self):
        """
        Tests edge deep copy.
        :return: None.
        """
        lhs = Edge(0, 1, EdgeType.UNDIRECTED)
        rhs = copy.deepcopy(lhs)

        assert lhs.i == rhs.i
        assert lhs.j == rhs.j
        assert lhs.type == rhs.type

        lhs.i = 3
        assert lhs.i != rhs.i
