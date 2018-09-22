import pandas as pd
from nose import with_setup
from nose.tools import assert_almost_equal

from pybbn.learn.data import DiscreteData


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


def get_good_df():
    """
    Gets a good dataframe.
    :return: Dataframe.
    """
    return pd.DataFrame({
        'x1': ['t', 't', 't', 't', 't', 'f', 'f', 'f', 'f', 'f'],
        'x2': ['t', 't', 't', 't', 'f', 't', 'f', 'f', 'f', 'f'],
        'x3': ['t', 't', 't', 't', 't', 't', 'f', 'f', 'f', 'f'],
        'x4': ['t', 't', 't', 't', 't', 'f', 'f', 'f', 'f', 'f']
    })


def get_bad_df():
    """
    Tests a bad dataframe.
    :return: Dataframe
    """
    return pd.DataFrame({
        'x1': ['t', 't', 't', 't', 't', 'f', 'f', 'f', 'f', 'f'],
        'x2': ['t', 't', 't', 't', 'f', 't', 'f', 'f', 'f', 'f'],
        'x3': ['t', 't', 't', 't', 't', 't', 'f', 'f', 'f', 'f'],
        'x4': ['t', 't', 't', 't', 't', 't', 't', 't', 't', 't']
    })


@with_setup(setup, teardown)
def test_count():
    """
    Tests simple counting.
    :return: None.
    """
    data = DiscreteData(get_good_df())
    assert 5 == data.__count__(['x1'], ['t'])
    assert 5 == data.__count__(['x1'], ['f'])

    assert 5 == data.__count__(['x2'], ['t'])
    assert 5 == data.__count__(['x2'], ['f'])

    assert 6 == data.__count__(['x3'], ['t'])
    assert 4 == data.__count__(['x3'], ['f'])

    assert 5 == data.__count__(['x4'], ['t'])
    assert 5 == data.__count__(['x4'], ['f'])


@with_setup(setup, teardown)
def test_count_parents_child():
    """
    Tests counting parent-child values.
    :return: None.
    """
    data = DiscreteData(get_good_df())

    assert 4 == data.__count_parents_child__('x1', 't', ['x2'], ['t'])
    assert 1 == data.__count_parents_child__('x1', 't', ['x2'], ['f'])
    assert 1 == data.__count_parents_child__('x1', 'f', ['x2'], ['t'])
    assert 4 == data.__count_parents_child__('x1', 'f', ['x2'], ['f'])


@with_setup(setup, teardown)
def test_get_local_kutato():
    """
    Tests computing local Kutato score.
    :return: None.
    """
    data = DiscreteData(get_good_df())

    assert_almost_equal(-1.540639, data.get_local_kutato('x1', ['x2']), places=5)
    assert_almost_equal(-1.540639, data.get_local_kutato('x2', ['x1']), places=5)

    assert_almost_equal(-1.082607, data.get_local_kutato('x1', ['x3']), places=5)
    assert_almost_equal(-1.124863, data.get_local_kutato('x3', ['x1']), places=5)

    assert_almost_equal(-0.709086, data.get_local_kutato('x1', ['x4']), places=5)
    assert_almost_equal(-0.709086, data.get_local_kutato('x4', ['x1']), places=5)


@with_setup(setup, teardown)
def test_is_valid_good():
    """
    Tests if a dataset is valid with a good dataframe.
    :return: None.
    """
    try:
        df = get_good_df()
        data = DiscreteData(df)
        assert 1 == 1
    except Exception:
        assert 1 == 2


@with_setup(setup, teardown)
def test_is_valid_bad():
    """
    Tests if a dataset is valid with a bad dataframe.
    :return: None.
    """
    try:
        df = get_bad_df()
        data = DiscreteData(df)
        assert 1 == 2
    except Exception:
        assert 1 == 1


@with_setup(setup, teardown)
def test_get_variable_profiles():
    """
    Tests getting variable profiles.
    :return: None.
    """
    data = DiscreteData(get_good_df())
    profiles = data.get_variable_profiles()

    print(data)
    assert 4 == len(profiles)

    for i in range(4):
        name = 'x{}'.format(i + 1)
        assert name in profiles

        profile = profiles[name]
        assert 't' in profile
        assert 'f' in profile


@with_setup(setup, teardown)
def test_sort():
    """
    Tests sorting names and values by names ascending.
    :return: None.
    """
    data = DiscreteData(get_good_df())
    observed = data.__sort__(['a', 'c', 'b', 'd'], ['t', 'f', 't', 'f'])
    expected = [('a', 't'), ('b', 't'), ('c', 'f'), ('d', 'f')]
    assert len(observed) == len(expected)
    for o, e in zip(observed, expected):
        assert o[0] == e[0]
        assert o[1] == e[1]


@with_setup(setup, teardown)
def test_to_query():
    """
    Tests generating query.
    :return: None.
    """
    data = DiscreteData(get_good_df())
    names = ['a', 'c', 'b', 'd']
    vals = ['t', 'f', 't', 'f']
    observed = data.__to_query__(names, vals)
    expected = 'a == "t" and b == "t" and c == "f" and d == "f"'
    assert observed == expected


@with_setup(setup, teardown)
def test_get_prob():
    """
    Gets getting simple probability.
    :return: None.
    """
    data = DiscreteData(get_good_df())
    assert_almost_equal(0.5, data.__get_prob__('x1', 't'))
    assert_almost_equal(0.5, data.__get_prob__('x1', 'f'))
    assert_almost_equal(0.5, data.__get_prob__('x2', 't'))
    assert_almost_equal(0.5, data.__get_prob__('x2', 'f'))
    assert_almost_equal(0.6, data.__get_prob__('x3', 't'))
    assert_almost_equal(0.4, data.__get_prob__('x3', 'f'))
    assert_almost_equal(0.5, data.__get_prob__('x4', 't'))
    assert_almost_equal(0.5, data.__get_prob__('x4', 'f'))


@with_setup(setup, teardown)
def test_get_joint_prob():
    """
    Tests getting joint probability between two variables.
    :return: None.
    """
    data = DiscreteData(get_good_df())

    assert_almost_equal(0.4, data.__get_joint_prob__('x1', 't', 'x2', 't'))
    assert_almost_equal(0.1, data.__get_joint_prob__('x1', 't', 'x2', 'f'))
    assert_almost_equal(0.1, data.__get_joint_prob__('x1', 'f', 'x2', 't'))
    assert_almost_equal(0.4, data.__get_joint_prob__('x1', 'f', 'x2', 'f'))


@with_setup(setup, teardown)
def test_get_joint_prob_set():
    """
    Tests getting joint probability between a variable and a set of variables.
    :return: None.
    """
    data = DiscreteData(get_good_df())

    assert_almost_equal(0.4, data.__get_joint_prob_set__('x1', 't', ['x2', 'x3'], ['t', 't']))
    assert_almost_equal(0.0, data.__get_joint_prob_set__('x1', 't', ['x2', 'x3'], ['t', 'f']))
    assert_almost_equal(0.1, data.__get_joint_prob_set__('x1', 't', ['x2', 'x3'], ['f', 't']))
    assert_almost_equal(0.0, data.__get_joint_prob_set__('x1', 't', ['x2', 'x3'], ['f', 'f']))

    assert_almost_equal(0.1, data.__get_joint_prob_set__('x1', 'f', ['x2', 'x3'], ['t', 't']))
    assert_almost_equal(0.0, data.__get_joint_prob_set__('x1', 'f', ['x2', 'x3'], ['t', 'f']))
    assert_almost_equal(0.0, data.__get_joint_prob_set__('x1', 'f', ['x2', 'x3'], ['f', 't']))
    assert_almost_equal(0.4, data.__get_joint_prob_set__('x1', 'f', ['x2', 'x3'], ['f', 'f']))


@with_setup(setup, teardown)
def test_get_joint_prob_triplet():
    """
    Tests getting joint probability between two variables and a set of variables.
    :return: None.
    """
    data = DiscreteData(get_good_df())

    assert_almost_equal(0.4, data.__get_joint_prob_triplet__('x1', 't', 'x2', 't', ['x3'], ['t']))
    assert_almost_equal(0.0, data.__get_joint_prob_triplet__('x1', 't', 'x2', 't', ['x3'], ['f']))
    assert_almost_equal(0.1, data.__get_joint_prob_triplet__('x1', 't', 'x2', 'f', ['x3'], ['t']))
    assert_almost_equal(0.0, data.__get_joint_prob_triplet__('x1', 't', 'x2', 'f', ['x3'], ['f']))

    assert_almost_equal(0.1, data.__get_joint_prob_triplet__('x1', 'f', 'x2', 't', ['x3'], ['t']))
    assert_almost_equal(0.0, data.__get_joint_prob_triplet__('x1', 'f', 'x2', 't', ['x3'], ['f']))
    assert_almost_equal(0.0, data.__get_joint_prob_triplet__('x1', 'f', 'x2', 'f', ['x3'], ['t']))
    assert_almost_equal(0.4, data.__get_joint_prob_triplet__('x1', 'f', 'x2', 'f', ['x3'], ['f']))


@with_setup(setup, teardown)
def test_get_cond_prob():
    """
    Tests getting conditional probability between two variables.
    :return: None.
    """
    data = DiscreteData(get_good_df())

    assert_almost_equal(0.8, data.__get_cond_prob__('x1', 't', 'x2', 't'))
    assert_almost_equal(0.2, data.__get_cond_prob__('x1', 't', 'x2', 'f'))
    assert_almost_equal(0.2, data.__get_cond_prob__('x1', 'f', 'x2', 't'))
    assert_almost_equal(0.8, data.__get_cond_prob__('x1', 'f', 'x2', 'f'))


@with_setup(setup, teardown)
def test_get_cond_prob_set():
    """
    Tests getting conditional probability between a variable and a set of variables.
    :return: None.
    """
    data = DiscreteData(get_good_df())

    assert_almost_equal(0.8, data.__get_cond_prob_set__('x1', 't', ['x2', 'x3'], ['t', 't']))
    assert_almost_equal(0.2, data.__get_cond_prob_set__('x1', 'f', ['x2', 'x3'], ['t', 't']))

    assert_almost_equal(0.0, data.__get_cond_prob_set__('x1', 't', ['x2', 'x3'], ['f', 'f']))
    assert_almost_equal(1.0, data.__get_cond_prob_set__('x1', 'f', ['x2', 'x3'], ['f', 'f']))

    assert_almost_equal(0.0, data.__get_cond_prob_set__('x1', 't', ['x2', 'x3'], ['t', 'f']))
    assert_almost_equal(0.0, data.__get_cond_prob_set__('x1', 'f', ['x2', 'x3'], ['t', 'f']))

    assert_almost_equal(1.0, data.__get_cond_prob_set__('x1', 't', ['x2', 'x3'], ['f', 't']))
    assert_almost_equal(0.0, data.__get_cond_prob_set__('x1', 'f', ['x2', 'x3'], ['f', 't']))


@with_setup(setup, teardown)
def test_get_cond_prob_triplet():
    """
    Tests getting conditional probability between two variables and a third set of variables.
    :return: None.
    """
    data = DiscreteData(get_good_df())

    assert_almost_equal(0.6666666666666667, data.__get_cond_prob_triplet__('x1', 't', 'x2', 't', ['x3'], ['t']))
    assert_almost_equal(0.0, data.__get_cond_prob_triplet__('x1', 't', 'x2', 't', ['x3'], ['f']))
    assert_almost_equal(0.16666666666666669, data.__get_cond_prob_triplet__('x1', 't', 'x2', 'f', ['x3'], ['t']))
    assert_almost_equal(0.0, data.__get_cond_prob_triplet__('x1', 't', 'x2', 'f', ['x3'], ['f']))

    assert_almost_equal(0.16666666666666669, data.__get_cond_prob_triplet__('x1', 'f', 'x2', 't', ['x3'], ['t']))
    assert_almost_equal(0.0, data.__get_cond_prob_triplet__('x1', 'f', 'x2', 't', ['x3'], ['f']))
    assert_almost_equal(0.0, data.__get_cond_prob_triplet__('x1', 'f', 'x2', 'f', ['x3'], ['t']))
    assert_almost_equal(1.0, data.__get_cond_prob_triplet__('x1', 'f', 'x2', 'f', ['x3'], ['f']))


@with_setup(setup, teardown)
def test_get_mi():
    """
    Tests getting mutual information.
    :return: None.
    """
    data = DiscreteData(get_good_df())

    assert_almost_equal(0.19274475702175753, data.__get_mi__('x1', 'x2'))
    assert_almost_equal(0.4228104552401625, data.__get_mi__('x1', 'x3'))
    assert_almost_equal(0.6931471805599453, data.__get_mi__('x1', 'x4'))
    assert_almost_equal(0.4228104552401625, data.__get_mi__('x2', 'x3'))
    assert_almost_equal(0.19274475702175753, data.__get_mi__('x2', 'x4'))
    assert_almost_equal(0.4228104552401625, data.__get_mi__('x3', 'x4'))


@with_setup(setup, teardown)
def test_get_cond_mi():
    """
    Tests getting conditional mutual information.
    :return: None.
    """
    data = DiscreteData(get_good_df())

    assert_almost_equal(0.0, data.__get_cond_mi__('x1', 'x2', ['x3', 'x4']))
    assert_almost_equal(0.0, data.__get_cond_mi__('x1', 'x3', ['x2', 'x4']))
    assert_almost_equal(0.25020121176909393, data.__get_cond_mi__('x1', 'x4', ['x2', 'x3']))

    assert_almost_equal(0.0, data.__get_cond_mi__('x2', 'x1', ['x3', 'x4']))
    assert_almost_equal(0.25020121176909393, data.__get_cond_mi__('x2', 'x3', ['x1', 'x4']))
    assert_almost_equal(0.0, data.__get_cond_mi__('x2', 'x4', ['x1', 'x3']))

    assert_almost_equal(0.0, data.__get_cond_mi__('x3', 'x1', ['x2', 'x4']))
    assert_almost_equal(0.25020121176909393, data.__get_cond_mi__('x3', 'x2', ['x1', 'x4']))
    assert_almost_equal(0.0, data.__get_cond_mi__('x3', 'x4', ['x1', 'x2']))

    assert_almost_equal(0.25020121176909393, data.__get_cond_mi__('x4', 'x1', ['x2', 'x3']))
    assert_almost_equal(0.0, data.__get_cond_mi__('x4', 'x2', ['x1', 'x3']))
    assert_almost_equal(0.0, data.__get_cond_mi__('x4', 'x3', ['x1', 'x2']))


@with_setup(setup, teardown)
def test_get_pairwise_mutual_information():
    """
    Tests get pairwise mutual information.
    :return: List of pairwise mutual information.
    """
    data = DiscreteData(get_good_df())
    observed = sorted(data.get_pairwise_mutual_information(), key=lambda tup: (-tup[2], tup[0], tup[1]))
    expected = [('x1', 'x4'), ('x1', 'x3'), ('x2', 'x3'), ('x3', 'x4'), ('x1', 'x2'), ('x2', 'x4')]

    print(observed)
    print('--')
    print(expected)

    assert len(observed) == len(expected)
    for o, e in zip(observed, expected):
        assert o[0] == e[0]
        assert o[1] == e[1]
