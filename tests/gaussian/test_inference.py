import random

import numpy as np
from nose import with_setup
from numpy.testing import assert_almost_equal

from pybbn.gaussian.inference import GaussianInference


def setup():
    """
    Setup.
    :return: None.
    """
    random.seed(37)
    np.random.seed(37)
    np.set_printoptions(
        precision=10,
        formatter={'float': lambda v: f'{v:.10f}'}
    )


def teardown():
    """
    Teardown.
    :return: None.
    """
    pass


def get_cowell_data():
    """
    Gets Cowell data.

    :return: Data and headers.
    """
    n = 10000
    Y = np.random.normal(0, 1, n)
    X = np.random.normal(Y, 1, n)
    Z = np.random.normal(X, 1, n)

    D = np.vstack([Y, X, Z]).T
    return D, ['Y', 'X', 'Z']


def get_castillo_data():
    """
    Gets Castillo data.

    :return: Data and headers.
    """
    n = 10000
    A = np.random.normal(0, 1, n)
    B = np.random.normal(0, 1, n)
    C = np.random.normal(A, 1, n)
    D = np.random.normal(0.2 * A + 0.8 * B, 1, n)

    E = np.vstack([A, B, C, D]).T
    return E, ['A', 'B', 'C', 'D']


@with_setup(setup, teardown)
def test_cowell_x():
    """
    Tests inference with Cowell example (X=1.5).
    """
    X, H = get_cowell_data()
    M = X.mean(axis=0)
    E = np.cov(X.T)

    g = GaussianInference(H, M, E)
    print(g.H)
    print(g.I)
    print(g.M)
    print(g.E)
    print('-' * 15)

    g = g.do_inference('X', 1.5)
    print(g.H)
    print(g.I)
    print(g.M)
    print(g.E)

    assert_almost_equal(g.M, [-0.7447794831, -1.5222039705])
    assert_almost_equal(g.E, [[0.4962114580, 0.0020891582],
                              [0.0020891582, 0.9843995081]])


@with_setup(setup, teardown)
def test_cowell_z():
    """
    Tests inference with Cowell example (z=1.5).
    """
    X, H = get_cowell_data()
    M = X.mean(axis=0)
    E = np.cov(X.T)

    g = GaussianInference(H, M, E)
    print(g.H)
    print(g.I)
    print(g.M)
    print(g.E)
    print('-' * 15)

    g = g.do_inference('Z', 1.5)
    print(g.H)
    print(g.I)
    print(g.M)
    print(g.E)

    assert_almost_equal(g.M, [-0.4978580082, -1.0141860551])
    assert_almost_equal(g.E, [[0.6552719951, 0.3226010216],
                              [0.3226010216, 0.6542698781]])


@with_setup(setup, teardown)
def test_cowell_y():
    """
    Tests inference with Cowell example (Y=1.5).
    """
    X, H = get_cowell_data()
    M = X.mean(axis=0)
    E = np.cov(X.T)

    g = GaussianInference(H, M, E)
    print(g.H)
    print(g.I)
    print(g.M)
    print(g.E)
    print('-' * 15)

    g = g.do_inference('Y', 1.5)
    print(g.H)
    print(g.I)
    print(g.M)
    print(g.E)

    assert_almost_equal(g.M, [-1.5175865285, -1.5280767750])
    assert_almost_equal(g.E, [[1.0099559400, 1.0160891744],
                              [1.0160891744, 2.0066503668]])


@with_setup(setup, teardown)
def test_castillo_abc():
    """
    Tests inference with Castillo example (A=1, B=2, C=3).
    """
    X, H = get_castillo_data()
    M = X.mean(axis=0)
    E = np.cov(X.T)

    g = GaussianInference(H, M, E)
    print(g.H)
    print(g.I)
    print(g.M)
    print(g.E)
    print('-' * 15)

    g = g.get_inference([('A', 1), ('B', 2), ('C', 3)])
    print(g.H)
    print(g.I)
    print(g.M)
    print(g.E)

    assert_almost_equal(g.M, [-1.8750908711])
    assert_almost_equal(g.E, [[1.0141480877]])
