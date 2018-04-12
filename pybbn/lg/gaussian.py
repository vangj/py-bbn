import math

import numpy as np
from numpy.linalg import inv, det
from scipy import linalg


def __get_box_muller_sample__():
    """
    Gets a sample using the Box-Muller transform.
    :return: A sample point.
    """
    r = 0
    x = 0
    y = 0

    while True:
        x = 2.0 * np.random.uniform(0.0, 1.0, 1)[0] - 1.0
        y = 2.0 * np.random.uniform(0.0, 1.0, 1)[0] - 1.0
        r = (x * x) + (y * y)

        if 0.0 < r <= 1.0:
            break

    z = x * math.sqrt(-2.0 * math.log(r) / r)
    return z


def __get_box_muller_samples__(n):
    """
    Gets n independent Box-Muller samples.
    :param n: Number of samples.
    :return: Array of Box-Muller samples of dimension 1 x n.
    """
    return np.array([__get_box_muller_sample__() for _ in range(n)])


def __get_sample__(m, s):
    """
    Sample from the Gaussian distribution with mean=m and standard
    deviation=s.
    :param m: Mean.
    :param s: Standard deviation.
    :return: Sample point.
    """
    z = __get_box_muller_sample__()
    return z * s + m


def __slice_acov__(cov, dep, given):
    """
    Slices a covariance matrix keeping only the row associated with the dependent variable
    minus its self-covariance.
    :param cov: Covariance matrix.
    :param dep: Index of dependent variable.
    :param given: Array of indices of independent variables.
    :return: A 1 x |given| vector of covariances.
    """
    row_selector = dep
    col_selector = [x for x in range(cov.shape[1]) if x in given]
    v = cov[row_selector, col_selector]
    return v


def __slice_scov__(cov, dep, given):
    """
    Slices a covariance matrix keeping only the covariances between the variables
    indicated by the array of indices of the independent variables.
    :param cov: Covariance matrix.
    :param dep: Index of dependent variable.
    :param given: Array of indices of independent variables.
    :return: A |given| x |given| matrix of covariance.
    """
    row_selector = [x for x in range(cov.shape[0]) if x in given and x != dep]
    col_selector = [x for x in range(cov.shape[1]) if x in given and x != dep]
    v = cov[row_selector, :]
    v = v[:, col_selector]
    return v


def rnorm(n, m, s):
    """
    Sample from the Gaussian distribution with mean=m and standard
    deviation=s.
    :param n: Number of samples.
    :param m: Mean.
    :param s: Standard deviation.
    :return: Sample points.
    """
    for i in range(n):
        yield __get_sample__(m, s)


def dnorm(data, m, s):
    """
    Gets the probability of each value in x given the mean=m and standard deviation=s.
    :param data: Array of values.
    :param m: Mean.
    :param s: Standard deviation.
    :return: Probabilities.
    """
    c = 1.0 / math.sqrt(2.0 * math.pi * math.pow(s, 2.0))
    d = 2.0 * math.pow(s, 2.0)
    for x in data:
        exponent = -1.0 * math.pow(x - m, 2.0) / d
        yield c * math.exp(exponent)


def rcmvnorm(n, m, cov, dep, given, X):
    """
    Samples from the conditional multivariate Gaussian distribution with means=m and
    covariance matrix=cov subject to the values X.
    :param n: The number of samples to generate.
    :param m: An array of means.
    :param cov: Covariance matrix.
    :param dep: Index of dependent variable.
    :param given: Array of indices of independent variables.
    :param X: Values of dependent variables.
    :return: Sample points.
    """
    # cov.rows should equal cov.cols
    # |m| should equal cov.rows
    # dep should be one integer
    # |given| should equal X.cols
    # |given| < cov.cols

    col_selector = [x for x in range(cov.shape[1]) if x in given]

    cov_yy = cov[dep, dep]
    cov_yx = __slice_acov__(cov, dep, given)
    cov_xx = inv(__slice_scov__(cov, dep, given))

    m_x = m[col_selector]
    m_y = m[dep]

    cov_yx_dot_cov_xx = cov_yx.dot(cov_xx)
    v_y = cov_yy - cov_yx.dot(cov_xx).dot(cov_yx.transpose())

    for i in range(n):
        e_y = m_y + cov_yx_dot_cov_xx.dot(X - m_x)
        y = list(rnorm(1, e_y, v_y))[0]
        yield y


def dcmvnorm(data, m, cov, dep, given):
    """
    Gets the probability of the dependent variable given the independent ones.
    :param data: Matrix of data.
    :param m: Array of means.
    :param cov: Covariance matrix.
    :param dep: Index of dependent variable.
    :param given: Array of indices of independent variables.
    :return: Probabilities.
    """
    # cov.rows should equal cov.cols
    # |m| should equal cov.rows
    # dep should be one integer
    # |given| should equal X.cols
    # |given| < cov.cols

    col_selector = [x for x in range(cov.shape[1]) if x in given]
    X = data[:, col_selector]
    y = data[:, dep]

    cov_yy = cov[dep, dep]
    cov_yx = __slice_acov__(cov, dep, given)
    cov_xx = inv(__slice_scov__(cov, dep, given))

    m_x = m[col_selector]
    m_y = m[dep]

    cov_yx_dot_cov_xx = cov_yx.dot(cov_xx)
    v_y = cov_yy - cov_yx.dot(cov_xx).dot(cov_yx.transpose())

    for i in range(data.shape[0]):
        e_y = m_y + cov_yx_dot_cov_xx.dot(X[i] - m_x)
        d = y[i]
        p_y = list(dnorm([d], e_y, v_y))[0]
        yield p_y


def rmvnorm(n, m, cov):
    """
    Samples from the multivariate Gaussian distribution with means=m and covariance matrix=cov.
    :param n: Number of samples.
    :param m: Array of means.
    :param cov: Covariance matrix.
    :return: Sample points.
    """
    A = linalg.cholesky(cov).transpose()
    v = cov.shape[0]
    for i in range(n):
        yield m + A.dot(__get_box_muller_samples__(v))


def dmvnorm(data, m, cov):
    """
    Computes the probabilities of the sample points in X.
    :param data: Data matrix.
    :param m: Means.
    :param cov: Covariance matrix.
    :return: Probabilities.
    """
    cov_inv = inv(cov)
    cov_det = det(cov)
    k = cov.shape[0]
    d = math.sqrt(math.pow(2.0 * math.pi, k) * cov_det)
    for i in range(data.shape[0]):
        x = data[i] - m
        y = x.reshape((k, 1))
        e = -0.5 * x.dot(cov_inv).dot(y)
        yield math.exp(e) / d


class RandCondMvn(object):
    """
    Random conditional multivariate normal.
    """

    def __init__(self, m, cov, dep, given):
        """
        Constructor.
        :param m: An array of means.
        :param cov: Covariance matrix.
        :param dep: Index of dependent variable.
        :param given: Array of indices of independent variables.
        :return: None.
        """
        # cov.rows should equal cov.cols
        # |m| should equal cov.rows
        # dep should be one integer
        # |given| should equal X.cols
        # |given| < cov.cols

        col_selector = [x for x in range(cov.shape[1]) if x in given]

        cov_yy = cov[dep, dep]
        cov_yx = __slice_acov__(cov, dep, given)
        cov_xx = inv(__slice_scov__(cov, dep, given))

        self.m_x = m[col_selector]
        self.m_y = m[dep]

        self.cov_yx_dot_cov_xx = cov_yx.dot(cov_xx)
        self.v_y = cov_yy - cov_yx.dot(cov_xx).dot(cov_yx.transpose())

    def next(self, X):
        """
        Samples from the conditional multivariate Gaussian distribution
        :param X: Values of dependent variables.
        :return: Sample.
        """
        e_y = self.m_y + self.cov_yx_dot_cov_xx.dot(X - self.m_x)
        y = list(rnorm(1, e_y, self.v_y))[0]
        return y
