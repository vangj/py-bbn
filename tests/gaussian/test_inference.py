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
    print(g.P)
    print('-' * 15)

    g = g.do_inference('X', 1.5)
    print(g.H)
    print(g.I)
    print(g.M)
    print(g.E)
    print(g.meta)
    print(g.P)

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
    print(g.meta)
    print(g.P)

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
    print(g.meta)
    print(g.P)

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
    print(g.meta)
    print(g.P)

    assert_almost_equal(g.M, [-1.8750908711])
    assert_almost_equal(g.E, [[1.0141480877]])


@with_setup(setup, teardown)
def test_repr():
    """
    Tests GaussianInference repr function.
    """
    X, H = get_castillo_data()
    M = X.mean(axis=0)
    E = np.cov(X.T)

    g = GaussianInference(H, M, E)
    print(g)
    o = str(g)
    e = 'GaussianInference[H=[A,B,C,D], M=[0.002,-0.009,0.007,-0.018], E=[[0.991,0.008,1.001,0.204]|[0.008,1.010,' \
        '0.014,0.799]|[1.001,0.014,1.996,0.225]|[0.204,0.799,0.225,1.685]], meta={}]'
    assert o == e

    print(g.marginals)
    o = g.marginals
    e = [{'name': 'A', 'mean': -0.0017234068142374496, 'var': 0.9907002440358944},
         {'name': 'B', 'mean': 0.009171006220968045, 'var': 1.0100180410420976},
         {'name': 'C', 'mean': -0.006711963688230272, 'var': 1.9957039315017837},
         {'name': 'D', 'mean': 0.018085596717747506, 'var': 1.6851371822157823}]
    assert len(e) == len(o)
    for act, obs in zip(e, o):
        assert act['name'] == obs['name']
        assert_almost_equal(act['mean'], obs['mean'])
        assert_almost_equal(act['var'], obs['var'])


@with_setup(setup, teardown)
def test_sample_marginals():
    """
    Tests sampling marginals.
    """
    X, H = get_castillo_data()
    M = X.mean(axis=0)
    E = np.cov(X.T)

    g = GaussianInference(H, M, E)
    print(g)

    e = [{'name': 'A', 'mean': -0.0017234068142374496, 'var': 0.9907002440358944},
         {'name': 'B', 'mean': 0.009171006220968045, 'var': 1.0100180410420976},
         {'name': 'C', 'mean': -0.006711963688230272, 'var': 1.9957039315017837},
         {'name': 'D', 'mean': 0.018085596717747506, 'var': 1.6851371822157823}]

    marginals = g.sample_marginals(size=10000)
    a = marginals['A']
    b = marginals['B']
    c = marginals['C']
    d = marginals['D']

    print(a.mean())
    print(b.mean())
    print(c.mean())
    print(d.mean())
    print('-' * 15)

    assert_almost_equal(a.mean(), e[0]['mean'], decimal=0.001)
    assert_almost_equal(b.mean(), e[1]['mean'], decimal=0.001)
    assert_almost_equal(c.mean(), e[2]['mean'], decimal=0.001)
    assert_almost_equal(d.mean(), e[3]['mean'], decimal=0.001)

    print(a.var())
    print(b.var())
    print(c.var())
    print(d.var())
    print('-' * 15)

    assert_almost_equal(a.var(), e[0]['var'], decimal=0.001)
    assert_almost_equal(b.var(), e[1]['var'], decimal=0.001)
    assert_almost_equal(c.var(), e[2]['var'], decimal=0.001)
    assert_almost_equal(d.var(), e[3]['var'], decimal=0.001)

    gg = g.do_inference('A', 0.0)
    print(gg.marginals)
    print('-' * 15)

    m = gg.sample_marginals()
    print(m['A'].mean(), m['A'].var())
    print(m['B'].mean(), m['B'].var())
    print(m['C'].mean(), m['C'].var())
    print(m['D'].mean(), m['D'].var())
