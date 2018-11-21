import json

from nose import with_setup

from pybbn.graph.factory import Factory
from pybbn.pptc.inferencecontroller import InferenceController


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


def get_json_string():
    return json.dumps(get_dict())


def get_dict():
    return {
        "V": ["Letter", "Grade", "Intelligence", "SAT", "Difficulty"],
        "E": [["Difficulty", "Grade"],
              ["Intelligence", "Grade"],
              ["Intelligence", "SAT"],
              ["Grade", "Letter"]],
        "Vdata": {
            "Letter": {
                "ord": 4,
                "numoutcomes": 2,
                "vals": ["weak", "strong"],
                "parents": ["Grade"],
                "children": None,
                "cprob": {
                    "['A']": [.1, .9],
                    "['B']": [.4, .6],
                    "['C']": [.99, .01]
                }
            },
            "SAT": {
                "ord": 3,
                "numoutcomes": 2,
                "vals": ["lowscore", "highscore"],
                "parents": ["Intelligence"],
                "children": None,
                "cprob": {
                    "['low']": [.95, .05],
                    "['high']": [.2, .8]
                }
            },
            "Grade": {
                "ord": 2,
                "numoutcomes": 3,
                "vals": ["A", "B", "C"],
                "parents": ["Difficulty", "Intelligence"],
                "children": ["Letter"],
                "cprob": {
                    "['easy', 'low']": [.3, .4, .3],
                    "['easy', 'high']": [.9, .08, .02],
                    "['hard', 'low']": [.05, .25, .7],
                    "['hard', 'high']": [.5, .3, .2]
                }
            },
            "Intelligence": {
                "ord": 1,
                "numoutcomes": 2,
                "vals": ["low", "high"],
                "parents": None,
                "children": ["SAT", "Grade"],
                "cprob": [.7, .3]
            },
            "Difficulty": {
                "ord": 0,
                "numoutcomes": 2,
                "vals": ["easy", "hard"],
                "parents": None,
                "children": ["Grade"],
                "cprob": [.6, .4]
            }
        }
    }


@with_setup(setup, teardown)
def test_from_libpgm_discrete_json():
    """
    Tests create py-bbn BBN from JSON string specifying libpgm BBN.
    :return: None.
    """
    j = get_json_string()
    bbn = Factory.from_libpgm_discrete_json(j)

    assert len(bbn.nodes) == 5
    assert len(bbn.edges) == 4


@with_setup(setup, teardown)
def test_from_libpgm_discrete_dictionary():
    """
    Tests create py-bbn BBN from dictionary specifying libpgm BBN.
    :return: None.
    """
    d = get_dict()
    bbn = Factory.from_libpgm_discrete_dictionary(d)

    assert len(bbn.nodes) == 5
    assert len(bbn.edges) == 4

    join_tree = InferenceController.apply(bbn)

    __validate_posterior__({
        'Difficulty': [0.6, 0.4],
        'Intelligence': [0.7, 0.3],
        'Grade': [0.362, 0.288, 0.350],
        'SAT': [0.725, 0.275],
        'Letter': [0.498, 0.502]
    }, join_tree, debug=True)


def __validate_posterior__(expected, join_tree, debug=False):
    for node in join_tree.get_bbn_nodes():
        potential = join_tree.get_bbn_potential(node)
        if debug is True:
            p = ', '.join(['{}'.format(e) for e in potential.entries])
            s = '{} : {}'.format(node.variable.name, p)
            print(s)

        o = [e.value for e in potential.entries]
        e = expected[node.variable.name]

        assert len(o) == len(e)
        for ob, ex in zip(o, e):
            diff = abs(ob - ex)
            if diff > 0.001 and debug:
                print('\t**observed={}, expected={}'.format(ob, ex))
            elif debug is False:
                assert diff < 0.001
