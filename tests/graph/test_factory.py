import json
import unittest

import pandas as pd

from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.factory import Factory
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController
from pybbn.sampling.sampling import LogicSampler


def get_json_string():
    return json.dumps(get_dict())


def get_dict():
    return {
        "V": ["Letter", "Grade", "Intelligence", "SAT", "Difficulty"],
        "E": [
            ["Difficulty", "Grade"],
            ["Intelligence", "Grade"],
            ["Intelligence", "SAT"],
            ["Grade", "Letter"],
        ],
        "Vdata": {
            "Letter": {
                "ord": 4,
                "numoutcomes": 2,
                "vals": ["weak", "strong"],
                "parents": ["Grade"],
                "children": None,
                "cprob": {
                    "['A']": [0.1, 0.9],
                    "['B']": [0.4, 0.6],
                    "['C']": [0.99, 0.01],
                },
            },
            "SAT": {
                "ord": 3,
                "numoutcomes": 2,
                "vals": ["lowscore", "highscore"],
                "parents": ["Intelligence"],
                "children": None,
                "cprob": {"['low']": [0.95, 0.05], "['high']": [0.2, 0.8]},
            },
            "Grade": {
                "ord": 2,
                "numoutcomes": 3,
                "vals": ["A", "B", "C"],
                "parents": ["Difficulty", "Intelligence"],
                "children": ["Letter"],
                "cprob": {
                    "['easy', 'low']": [0.3, 0.4, 0.3],
                    "['easy', 'high']": [0.9, 0.08, 0.02],
                    "['hard', 'low']": [0.05, 0.25, 0.7],
                    "['hard', 'high']": [0.5, 0.3, 0.2],
                },
            },
            "Intelligence": {
                "ord": 1,
                "numoutcomes": 2,
                "vals": ["low", "high"],
                "parents": None,
                "children": ["SAT", "Grade"],
                "cprob": [0.7, 0.3],
            },
            "Difficulty": {
                "ord": 0,
                "numoutcomes": 2,
                "vals": ["easy", "hard"],
                "parents": None,
                "children": ["Grade"],
                "cprob": [0.6, 0.4],
            },
        },
    }


def __validate_posterior__(expected, join_tree, debug=False):
    for node in join_tree.get_bbn_nodes():
        potential = join_tree.get_bbn_potential(node)
        if debug is True:
            p = ", ".join(["{}".format(e) for e in potential.entries])
            s = "{} : {}".format(node.variable.name, p)
            print(s)

        o = [e.value for e in potential.entries]
        e = expected[node.variable.name]

        assert len(o) == len(e)
        for ob, ex in zip(o, e):
            diff = abs(ob - ex)
            if diff > 0.001 and debug:
                print("\t**observed={}, expected={}".format(ob, ex))
            elif debug is False:
                assert diff < 0.001


class TestFactory(unittest.TestCase):
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

    def test_from_libpgm_discrete_json(self):
        """
        Tests create py-bbn BBN from JSON string specifying libpgm BBN.
        :return: None.
        """
        j = get_json_string()
        bbn = Factory.from_libpgm_discrete_json(j)

        assert len(bbn.nodes) == 5
        assert len(bbn.edges) == 4

    def test_from_libpgm_discrete_dictionary(self):
        """
        Tests create py-bbn BBN from dictionary specifying libpgm BBN.
        :return: None.
        """
        d = get_dict()
        bbn = Factory.from_libpgm_discrete_dictionary(d)

        assert len(bbn.nodes) == 5
        assert len(bbn.edges) == 4

        join_tree = InferenceController.apply(bbn)

        __validate_posterior__(
            {
                "Difficulty": [0.6, 0.4],
                "Intelligence": [0.7, 0.3],
                "Grade": [0.362, 0.288, 0.350],
                "SAT": [0.725, 0.275],
                "Letter": [0.498, 0.502],
            },
            join_tree,
            debug=True,
        )

    def test_from_data_simple(self):
        """
        Tests create BBN from data.
        :return: None.
        """
        a = BbnNode(Variable(0, "a", ["on", "off"]), [0.5, 0.5])
        b = BbnNode(Variable(1, "b", ["on", "off"]), [0.5, 0.5, 0.4, 0.6])
        c = BbnNode(Variable(2, "c", ["on", "off"]), [0.7, 0.3, 0.2, 0.8])

        bbn1 = (
            Bbn()
            .add_node(a)
            .add_node(b)
            .add_node(c)
            .add_edge(Edge(a, b, EdgeType.DIRECTED))
            .add_edge(Edge(b, c, EdgeType.DIRECTED))
        )

        sampler = LogicSampler(bbn1)
        samples = sampler.get_samples(n_samples=10000, seed=37)

        i2n = {n.variable.id: n.variable.name for n in bbn1.get_nodes()}
        samples = pd.DataFrame(samples).rename(columns=i2n)

        parents = {"a": [], "b": ["a"], "c": ["b"]}

        bbn2 = Factory.from_data(parents, samples)

        join_tree1 = InferenceController.apply(bbn1)
        join_tree2 = InferenceController.apply(bbn2)

        posteriors1 = join_tree1.get_posteriors()
        posteriors2 = join_tree2.get_posteriors()

        for k, v1 in posteriors1.items():
            assert k in posteriors2

            v2 = posteriors2[k]
            assert len(v1) == len(v2)

            for k2 in v1:
                assert k2 in v2
                diff = abs(v1[k2] - v2[k2])
                assert diff < 0.01

    def test_ordered(self):
        """
        Tests learn parameters from DataFrame when columns of DataFrame are ordered.
        :return: None.
        """
        df = pd.DataFrame(
            [
                ["0", "1", "0", "0"],
                ["1", "0", "1", "1"],
                ["1", "0", "1", "1"],
                ["1", "0", "0", "0"],
                ["2", "1", "1", "2"],
            ],
            columns=["a", "b", "c", "d"],
        )
        structure = {"a": [], "b": ["a"], "c": ["a"], "d": ["b", "c"]}

        bbn = Factory.from_data(structure, df)
        jt = InferenceController.apply(bbn)

        observed = jt.get_posteriors()
        observed = {
            k: v
            for k, v in sorted(
                [(k, v) for k, v in observed.items()], key=lambda tup: tup[0]
            )
        }

        expected = {
            "a": {"0": 0.2, "1": 0.60, "2": 0.2},
            "b": {"0": 0.60, "1": 0.4},
            "c": {"0": 0.4, "1": 0.60},
            "d": {"0": 0.4, "1": 0.4, "2": 0.2},
        }

        for k in expected:
            assert k in observed
            for v in expected[k]:
                assert v in observed[k]
                assert expected[k][v] - observed[k][v] < 1e-5

        # import json
        # print(json.dumps(observed, indent=1))

    def test_not_ordered(self):
        """
        Tests learning parameters from DataFrame when columns are not ordered.
        :return: None.
        """
        # instead of the columns being: a, b, c, d
        # now we swap b and c: a, c, b, d
        # the order of the columns in the dataframe should not affect learning the parameters
        # this is the same unit test as above with simply rearranging the columns
        df = pd.DataFrame(
            [
                ["0", "1", "0", "0"],
                ["1", "0", "1", "1"],
                ["1", "0", "1", "1"],
                ["1", "0", "0", "0"],
                ["2", "1", "1", "2"],
            ],
            columns=["a", "b", "c", "d"],
        )[["a", "c", "b", "d"]]
        structure = {"a": [], "b": ["a"], "c": ["a"], "d": ["b", "c"]}

        bbn = Factory.from_data(structure, df)
        jt = InferenceController.apply(bbn)

        observed = jt.get_posteriors()
        observed = {
            k: v
            for k, v in sorted(
                [(k, v) for k, v in observed.items()], key=lambda tup: tup[0]
            )
        }

        expected = {
            "a": {"0": 0.2, "1": 0.60, "2": 0.2},
            "b": {"0": 0.60, "1": 0.4},
            "c": {"0": 0.4, "1": 0.60},
            "d": {"0": 0.4, "1": 0.4, "2": 0.2},
        }

        for k in expected:
            assert k in observed
            for v in expected[k]:
                assert v in observed[k]
                assert expected[k][v] - observed[k][v] < 1e-5
