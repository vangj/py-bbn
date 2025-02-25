import unittest

from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.node import Node
from pybbn.graph.pdag import Pdag


class TestPDag(unittest.TestCase):
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

    def test_pdag_creation(self):
        """
        Tests PDAG creation.
        :return:
        """
        n0 = Node(0)
        n1 = Node(1)
        n2 = Node(2)
        e0 = Edge(n0, n1, EdgeType.DIRECTED)
        e1 = Edge(n1, n2, EdgeType.DIRECTED)
        e2 = Edge(n2, n0, EdgeType.DIRECTED)

        g = Pdag()
        g.add_node(n0)
        g.add_node(n1)
        g.add_edge(e0)
        g.add_edge(e1)
        g.add_edge(e2)

        print(g)

        assert len(g.get_nodes()) == 3
        assert len(g.get_edges()) == 2

        assert len(list(g.get_neighbors(0))) == 1
        assert len(list(g.get_neighbors(1))) == 2
        assert len(list(g.get_neighbors(2))) == 1

        assert 1 in g.get_neighbors(0)
        assert 0 in g.get_neighbors(1)
        assert 2 in g.get_neighbors(1)
        assert 1 in g.get_neighbors(2)

        assert g.edge_exists(0, 1) == 1
        assert g.edge_exists(1, 2) == 1
        assert g.edge_exists(0, 2) == 0

        assert g.directed_edge_exists(0, 1) == 1
        assert g.directed_edge_exists(1, 2) == 1
        assert g.directed_edge_exists(0, 2) == 0

        assert len(g.get_parents(0)) == 0
        assert len(g.get_parents(1)) == 1
        assert len(g.get_parents(2)) == 1

        assert 0 in g.get_parents(1)
        assert 1 in g.get_parents(2)

        assert len(g.get_out_nodes(0)) == 1
        assert len(g.get_out_nodes(1)) == 1
        assert len(g.get_out_nodes(2)) == 0

        assert 1 in g.get_out_nodes(0)
        assert 2 in g.get_out_nodes(1)
