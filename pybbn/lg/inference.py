import warnings
from collections import namedtuple

import numpy as np
from numpy.linalg import inv
from numpy.random import multivariate_normal, normal
from scipy.stats import multivariate_normal as mvn_normal

COV = namedtuple('COV', 'C11 C12 C21 C22 C22I')


def __compute_means__(v, M, C, i1, i2):
    """
    Computes the conditional means.

    :param v: The values conditioned on.
    :param M: Marginal means (vector).
    :param C: Covariance matrix.
    :param i1: Indices of unconditioned variables.
    :param i2: Indices of conditioned variables.
    :return: Conditional means.
    """
    return M[i1] + C.C12.dot(C.C22I).dot(v - M[i2])


def __compute_covs__(C):
    """
    Computes the conditional covariance matrix.

    :param C: Partitioned covariance matrix.
    :return: Conditional covariance matrix.
    """
    return C.C11 - C.C12.dot(C.C22I).dot(C.C21)


def __update_mean__(m, v, M, i1, i2):
    """
    Updates the means.

    :param m: Means of unconditioned variables.
    :param v: Means of conditioned variables.
    :param M: Vector of marginal means.
    :param i1: Indices of unconditioned variables.
    :param i2: Indices of conditioned variables.
    :return: Updated means.
    """
    M_u = np.copy(M)
    for i, mu in zip(i1, m):
        M_u[i] = mu
    for i, mu in zip(i2, v):
        M_u[i] = mu
    return M_u


def __update_cov__(c, S, i1, i2):
    """
    Updates the covariance matrix.

    :param c: Conditioned covariance matrix.
    :param S: Covariance matrix.
    :param i1: Indices of unconditioned variables.
    :param i2: Indices of conditioned variables.
    :return: Updated covariance matrix.
    """
    m = np.copy(S)
    rows, cols = c.shape
    for row in range(rows):
        for col in range(cols):
            m[i1[row], i1[col]] = c[row, col]
    for i in i2:
        m[i, i] = 0.01
    return m


def __to_row_indices__(indices):
    """
    Creates row indices for help in broadcasting/slicing matrix.

    :param indices: Indices.
    :return: Array of array of indices.
    """
    return [[i] for i in indices]


def __to_col_indices__(indices):
    """
    Creates column indices for help in broadcasting/slicing matrix.

    :param indices: Indices.
    :return: Array.
    """
    return indices


def get_covariances(i1, i2, S):
    """
    Gets the partitioned matrices of S.

    :param i1: Indices of unconditioned variables.
    :param i2: Indices of conditioned variables.
    :param S: Covariance matrix.
    :return: Partitioned matrices of S.
    """
    r = __to_row_indices__(i1)
    c = __to_col_indices__(i1)
    C11 = S[r, c]

    r = __to_row_indices__(i1)
    c = __to_col_indices__(i2)
    C12 = S[r, c]

    r = __to_row_indices__(i2)
    c = __to_col_indices__(i1)
    C21 = S[r, c]

    r = __to_row_indices__(i2)
    c = __to_col_indices__(i2)
    C22 = S[r, c]

    C22I = inv(C22)

    return COV(C11, C12, C21, C22, C22I)


class MvnInference(object):
    """
    Multivariate normal Gaussian.
    """

    def __init__(self, M, S, N=10000):
        """
        Ctor.

        :param M: Vector of means.
        :param S: Matrix of covariances.
        :param N: Number of samples (default: 10,000).
        """
        self.M = M
        self.S = S
        self.N = N
        self.M_u = None
        self.S_u = None

    def clear(self):
        """
        Clears the updated mean and covariance.

        :return: None.
        """
        self.M_u = None
        self.S_u = None

    def update_mean_cov(self, v, iv):
        """
        Updates the means and covariances.

        :param v: Values conditioned.
        :param iv: Indices of variables conditioned on.
        :return: None.
        """
        if v is None or iv is None or len(v) == 0 or len(iv) == 0:
            self.M_u = np.copy(self.M)
            self.S_u = np.copy(self.S)
            return

        if self.M.shape[0] == 1:
            self.M_u = np.array([v[0]])
            self.S_u = 0.01
            return

        i2 = iv.copy()
        i1 = [i for i in range(self.S.shape[0]) if i not in i2]

        C = get_covariances(i1, i2, self.S)
        m = __compute_means__(v, self.M, C, i1, i2)
        c = __compute_covs__(C)
        self.M_u = __update_mean__(m, v, self.M, i1, i2)
        self.S_u = __update_cov__(c, self.S, i1, i2)

    def get_params(self):
        """
        Gets the means and covariances.

        :return: (means, covariances).
        """
        return (self.M, self.S) if self.M_u is None or self.S_u is None else (self.M_u, self.S_u)

    def get_samples(self):
        """
        Gets drawn samples from the current means and covariances.

        :return:
        """
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            M, S = self.get_params()

            if M.shape[0] == 1:
                return normal(M[0], S, self.N)

            return multivariate_normal(M, S, self.N)

    def get_corr(self):
        """
        Estimates the pair-wise correlation between all variables
        using drawn samples from the means and covariances.

        :return: Pairwise correlation matrix.
        """
        return np.corrcoef(self.get_samples().T)

    def predict_proba(self, X):
        """
        Predicts the probabilities.

        :param X: Data.
        :return: Probabilities.
        """
        M, S = self.get_params()
        return multivariate_normal.pdf(X, mean=M, cov=S)

    def predict_log_proba(self, X):
        """
        Predicts the log probabilities.

        :param X: Data.
        :return: Log probabilities.
        """
        M, S = self.get_params()
        return mvn_normal.logpdf(X, mean=M, cov=S)
