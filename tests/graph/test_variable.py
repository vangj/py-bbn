import copy
import unittest

from pybbn.graph.variable import Variable


class TestVariable(unittest.TestCase):
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
        Tests variable copy.
        :return: None.
        """
        lhs = Variable(0, "a", ["t", "f"])
        rhs = copy.copy(lhs)

        assert lhs.id == rhs.id
        assert lhs.name == rhs.name
        assert len(lhs.values) == len(rhs.values)
        for lhs_v, rhs_v in zip(lhs.values, rhs.values):
            assert lhs_v == rhs_v

        lhs.values[0] = "true"
        assert lhs.values[0] == rhs.values[0]

    def test_deep_copy(self):
        """
        Tests variable deepcopy.
        :return: None.
        """
        lhs = Variable(0, "a", ["t", "f"])
        rhs = copy.deepcopy(lhs)

        assert lhs.id == rhs.id
        assert lhs.name == rhs.name
        assert len(lhs.values) == len(rhs.values)
        for lhs_v, rhs_v in zip(lhs.values, rhs.values):
            assert lhs_v == rhs_v

        lhs.values[0] = "true"
        assert lhs.values[0] != rhs.values[0]
