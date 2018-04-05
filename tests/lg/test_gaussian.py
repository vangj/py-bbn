import math

import numpy as np
from nose import with_setup
from nose.tools import assert_almost_equal
from scipy.stats import norm

from pybbn.lg.gaussian import __get_sample__, rnorm, dnorm, rmvnorm, dmvnorm, rcmvnorm, dcmvnorm


def setup():
    """
    Setup.
    :return: None.
    """
    np.random.seed(37)


def teardown():
    """
    Teardown.
    :return: None.
    """
    pass


@with_setup(setup, teardown)
def test_gaussian_sampling():
    """
    Tests Gaussian sampling.
    :return: None.
    """
    mean, stdev = 3, 10
    samples = np.asarray([__get_sample__(mean, stdev) for _ in range(9000)])
    m, s = samples.mean(), math.sqrt(samples.var())
    print('m={}, s={}'.format(m, s))
    assert_almost_equal(mean, m, delta=0.1)
    assert_almost_equal(stdev, s, delta=0.1)


@with_setup(setup, teardown)
def test_rnorm():
    """
    Tests sampling from Gaussian distribution.
    :return: None.
    """
    mean, stdev = 3, 10
    samples = np.asarray(list(rnorm(9000, mean, stdev)))
    m, s = samples.mean(), math.sqrt(samples.var())
    print('m={}, s={}'.format(m, s))
    assert_almost_equal(mean, m, delta=0.1)
    assert_almost_equal(stdev, s, delta=0.1)


@with_setup(setup, teardown)
def test_dnorm():
    """
    Tests computing probabilities of values for a Gaussian distribution.
    :return: None.
    """
    mean, stdev = 3, 10
    samples = np.asarray(list(rnorm(9000, mean, stdev)))

    prob_a = sum(np.log(np.asarray(list(dnorm(samples, mean, stdev)))))
    prob_b = sum(np.log(norm.pdf(samples, mean, stdev)))
    assert_almost_equal(prob_a, prob_b, delta=0.01)


@with_setup(setup, teardown)
def test_rmvnorm():
    """
    Tests sampling from multivariate Gaussian distribution.
    :return: None.
    """
    samples = np.array(list(rmvnorm(
        90000,
        np.array([0.0, 25.0]),
        np.array([
            [1.091385, 1.949606],
            [1.949606, 4.520746]]))
    ))
    means = samples.mean(axis=0)
    x_mean, y_means = means[0], means[1]
    assert_almost_equal(x_mean, 0.0, delta=0.01)
    assert_almost_equal(y_means, 25.0, delta=0.01)


@with_setup(setup, teardown)
def test_dmvnorm():
    """
    Tests computing probabilities of values for a multivariate Gaussian distribution.
    :return: None.
    """
    p1 = sum(np.log(np.array(list(dmvnorm(
        data=np.array([[0, 25], [1, 26], [0, 26]]),
        m=np.array([0.0, 25.0]),
        cov=np.array([
            [1.091385, 1.949606],
            [1.949606, 4.520746]])
    )))))
    assert_almost_equal(p1, -6.938470946099255, places=1)

    p2 = sum(np.log(np.array(list(dmvnorm(
        data=np.array([[0, 25], [1, 26], [0, 27]]),
        m=np.array([0.0, 25.0]),
        cov=np.array([
            [1.091385, 1.949606],
            [1.949606, 4.520746]])
    )))))
    assert_almost_equal(p2, -8.383489807272817, places=1)

    assert p1 > p2


@with_setup(setup, teardown)
def test_rcmvnorm():
    """
    Tests sampling from a conditional multivariate Gaussian distribution.
    :return: None.
    """
    m = np.array(list(rcmvnorm(
        9000,
        np.array([0, 25]),
        np.array([[1.09, 1.95], [1.95, 4.52]]),
        1,
        [0],
        np.array([1])))).mean()
    assert_almost_equal(m, 26.793937408775005, places=1)

    m = np.array(list(rcmvnorm(
        90000,
        np.array([0, 25]),
        np.array([[1.09, 1.95], [1.95, 4.52]]),
        1,
        [0],
        np.array([0])))).mean()
    assert_almost_equal(m, 25.000056049420696, places=1)

    m = np.array(list(rcmvnorm(
        90000,
        np.array([0, 25]),
        np.array([[1.09, 1.95], [1.95, 4.52]]),
        0,
        [1],
        np.array([20])))).mean()
    assert_almost_equal(m, -2.156362075970362, delta=0.01)


@with_setup(setup, teardown)
def test_dcmvnorm():
    """
    Tests computing probabilities of values for a conditional multivariate Gaussian distribution.
    :return: None.
    """
    p1 = sum(np.log(np.array(list(dcmvnorm(
        data=np.array([
            [0, 25],
            [0, 25],
            [0, 24],
            [1, 26],
            [1, 25]
        ]),
        m=np.array([0, 25]),
        cov=np.array([[1.09, 1.95], [1.95, 4.52]]),
        dep=1,
        given=[0]
    )))))
    assert_almost_equal(p1, -7.0162097830845696, places=1)

    p2 = sum(np.log(np.array(list(dcmvnorm(
        data=np.array([
            [0, 25],
            [0, 25],
            [0, 24],
            [1, 25],
            [1, 25]
        ]),
        m=np.array([0, 25]),
        cov=np.array([[1.09, 1.95], [1.95, 4.52]]),
        dep=1,
        given=[0]
    )))))
    assert_almost_equal(p2, -8.227751578381055, places=2)

    assert p1 > p2
