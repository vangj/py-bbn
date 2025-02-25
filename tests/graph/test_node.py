import copy
import unittest

from pybbn.graph.node import BbnNode, Clique, Node
from pybbn.graph.variable import Variable


class TestNode(unittest.TestCase):
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

    def test_node_copy(self):
        """
        Tests node copy.
        :return: None.
        """
        lhs = Node(1)
        rhs = copy.copy(lhs)

        assert lhs.id == rhs.id

        lhs.id = 0
        assert lhs.id != rhs.id

    def test_node_deepcopy(self):
        """
        Tests node deep copy.
        :return: None.
        """
        lhs = Node(1)
        rhs = copy.deepcopy(lhs)

        assert lhs.id == rhs.id

        lhs.id = 0
        assert lhs.id != rhs.id

    def test_bbn_node_copy(self):
        """
        Tests BBN node copy.
        :return: None.
        """
        lhs = BbnNode(Variable(0, "a", ["t", "f"]), [0.2, 0.8])
        rhs = copy.copy(lhs)

        assert lhs.variable.id == rhs.variable.id
        assert lhs.variable.name == rhs.variable.name
        assert len(lhs.variable.values) == len(rhs.variable.values)
        for lhs_v, rhs_v in zip(lhs.variable.values, rhs.variable.values):
            assert lhs_v == rhs_v
        assert len(lhs.probs) == len(rhs.probs)
        for lhs_v, rhs_v in zip(lhs.probs, rhs.probs):
            self.assertAlmostEqual(lhs_v, rhs_v, 3)

        lhs.variable.values[0] = "true"
        assert lhs.variable.values[0] == rhs.variable.values[0]

    def test_bbn_node_deepcopy(self):
        """
        Tests BBN deep copy.
        :return: None.
        """
        lhs = BbnNode(Variable(0, "a", ["t", "f"]), [0.2, 0.8])
        rhs = copy.deepcopy(lhs)

        assert lhs.variable.id == rhs.variable.id
        assert lhs.variable.name == rhs.variable.name
        assert len(lhs.variable.values) == len(rhs.variable.values)
        for lhs_v, rhs_v in zip(lhs.variable.values, rhs.variable.values):
            assert lhs_v == rhs_v
        assert len(lhs.probs) == len(rhs.probs)
        for lhs_v, rhs_v in zip(lhs.probs, rhs.probs):
            self.assertAlmostEqual(lhs_v, rhs_v, 3)

        lhs.variable.values[0] = "true"
        assert lhs.variable.values[0] != rhs.variable.values[0]

    def test_bbn_node_creation(self):
        """
        Tests BBN node creation.
        :return: None.
        """
        a = BbnNode(Variable(0, "a", ["on", "off"]), [0.5, 0.5])
        b = BbnNode(Variable(1, "b", ["on", "off"]), [0.5, 0.5, 0.4, 0.6])
        c = BbnNode(Variable(2, "c", ["on", "off"]), [0.7, 0.3, 0.2, 0.8])
        d = BbnNode(Variable(3, "d", ["on", "off"]), [0.9, 0.1, 0.5, 0.5])
        e = BbnNode(Variable(4, "e", ["on", "off"]), [0.3, 0.7, 0.6, 0.4])
        f = BbnNode(
            Variable(5, "f", ["on", "off"]),
            [0.01, 0.99, 0.01, 0.99, 0.01, 0.99, 0.99, 0.01],
        )
        g = BbnNode(Variable(6, "g", ["on", "off"]), [0.8, 0.2, 0.1, 0.9])
        h = BbnNode(
            Variable(7, "h", ["on", "off"]),
            [0.05, 0.95, 0.95, 0.05, 0.95, 0.05, 0.95, 0.05],
        )

        assert a.id == 0
        assert b.id == 1
        assert c.id == 2
        assert d.id == 3
        assert e.id == 4
        assert f.id == 5
        assert g.id == 6
        assert h.id == 7

        assert a.get_weight() == 2
        assert b.get_weight() == 2
        assert c.get_weight() == 2
        assert d.get_weight() == 2
        assert e.get_weight() == 2
        assert f.get_weight() == 2
        assert g.get_weight() == 2
        assert h.get_weight() == 2

    def test_clique_creation(self):
        """
        Tests clique creation.
        :return: None.
        """
        a = BbnNode(Variable(0, "a", ["on", "off"]), [0.5, 0.5])
        b = BbnNode(Variable(1, "b", ["on", "off"]), [0.5, 0.5, 0.4, 0.6])
        c = BbnNode(Variable(2, "c", ["on", "off"]), [0.7, 0.3, 0.2, 0.8])
        clique = Clique([a, b, c])

        assert clique.id == "0-1-2"
        assert len(clique.nodes) == 3
        assert clique.get_weight() == 8
        assert clique.contains(0)
        assert clique.contains(1)
        assert clique.contains(2)
        assert clique.contains(3) == 0

    def test_clique_is_superset(self):
        """
        Tests if clique is a superset of another clique.
        :return: None.
        """
        a = BbnNode(Variable(0, "a", ["on", "off"]), [0.5, 0.5])
        b = BbnNode(Variable(1, "b", ["on", "off"]), [0.5, 0.5, 0.4, 0.6])
        c = BbnNode(Variable(2, "c", ["on", "off"]), [0.7, 0.3, 0.2, 0.8])
        d = BbnNode(Variable(3, "d", ["on", "off"]), [0.9, 0.1, 0.5, 0.5])

        abc = Clique([a, b, c])
        abc2 = Clique([a, b, c])
        ab = Clique([a, b])
        ac = Clique([a, c])
        bc = Clique([b, c])
        cd = Clique([c, d])

        assert abc.is_superset(Clique([a])) == 1
        assert abc.is_superset(Clique([b])) == 1
        assert abc.is_superset(Clique([c])) == 1
        assert abc.is_superset(Clique([d])) == 0
        assert abc.is_superset(abc2) == 1
        assert abc.is_superset(ab) == 1
        assert abc.is_superset(ac) == 1
        assert abc.is_superset(bc) == 1
        assert abc.is_superset(cd) == 0

    def test_sep_set_creation(self):
        """
        Tests separation set creation.
        :return: None.
        """
        a = BbnNode(Variable(0, "a", ["on", "off"]), [0.5, 0.5])
        b = BbnNode(Variable(1, "b", ["on", "off"]), [0.5, 0.5, 0.4, 0.6])
        c = BbnNode(Variable(2, "c", ["on", "off"]), [0.7, 0.3, 0.2, 0.8])
        d = BbnNode(Variable(3, "d", ["on", "off"]), [0.9, 0.1, 0.5, 0.5])
        abc = Clique([a, b, c])
        bcd = Clique([b, c, d])
        sepset = abc.get_sep_set(bcd)

        assert len(sepset.nodes) == 2

        names = [node.variable.name for node in sepset.nodes]
        assert "b" in names
        assert "c" in names

        assert sepset.get_cost() == 16
        assert sepset.get_mass() == 2

    def test_str(self):
        """
        Tests str function.
        :return: None.
        """
        a = BbnNode(Variable(0, "a", ["on", "off"]), [0.5, 0.5])
        b = BbnNode(Variable(1, "b", ["on", "off"]), [0.5, 0.5, 0.4, 0.6])
        c = BbnNode(Variable(2, "c", ["on", "off"]), [0.7, 0.3, 0.2, 0.8])
        d = BbnNode(Variable(3, "d", ["on", "off"]), [0.9, 0.1, 0.5, 0.5])
        abc = Clique([a, b, c])
        bcd = Clique([b, c, d])
        sepset = abc.get_sep_set(bcd)

        print(a)
        print(b)
        print(c)
        print(d)
        print(abc)
        print(bcd)
        print(sepset)

        assert a.__str__() == "0|a|on,off"
        assert b.__str__() == "1|b|on,off"
        assert c.__str__() == "2|c|on,off"
        assert d.__str__() == "3|d|on,off"
        assert abc.__str__() == "(a,b,c)"
        assert bcd.__str__() == "(b,c,d)"
        assert sepset.__str__() == "|(a,b,c) -- b,c -- (b,c,d)|"
