import numpy as np
from collections import namedtuple
from numpy.linalg import inv
from numpy.random import multivariate_normal
import warnings

COV = namedtuple('COV', 'C11 C12 C21 C22 C22I')


def __compute_means__(a, M, C, i1, i2):
    a = np.array([2.0])
    return M[i1] + C.C12.dot(C.C22I).dot(a - M[i2])


def __compute_covs__(C):
    return C.C11 - C.C12.dot(C.C22I).dot(C.C21)


def __update_mean__(m, a, M, i1, i2):
    v = np.copy(M)
    for i, mu in zip(i1, m):
        v[i] = mu
    for i, mu in zip(i2, a):
        v[i] = mu
    return v


def __update_cov__(c, S, i1, i2):
    m = np.copy(S)
    rows, cols = c.shape
    for row in range(rows):
        for col in range(cols):
            m[i1[row], i1[col]] = c[row, col]
    for i in i2:
        m[i, i] = 0.01
    return m


def __to_row_indices__(indices):
    return [[i] for i in indices]


def __to_col_indices__(indices):
    return indices


def get_covariances(i1, i2, S):
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


class MvnGaussian(object):

    def __init__(self, M, S, N=10000):
        self.M = M
        self.S = S
        self.N = N
        self.M_u = None
        self.S_u = None

    def clear(self):
        self.M_u = None
        self.S_u = None

    def update_mean_cov(self, v, iv):
        if v is None or iv is None or len(v) == 0 or len(iv) == 0:
            self.M_u = np.copy(self.M)
            self.S_u = np.copy(self.S)
            return

        i2 = iv.copy()
        i1 = [i for i in range(self.S.shape[0]) if i not in i2]

        C = get_covariances(i1, i2, self.S)
        m = __compute_means__(v, self.M, C, i1, i2)
        c = __compute_covs__(C)
        self.M_u = __update_mean__(m, v, self.M, i1, i2)
        self.S_u = __update_cov__(c, self.S, i1, i2)

    def get_params(self):
        return (self.M, self.S) if self.M_u is None or self.S_u is None else (self.M_u, self.S_u)

    def get_samples(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            M, S = self.get_params()
            return multivariate_normal(M, S, self.N)

    def get_corr(self):
        return np.corrcoef(self.get_samples().T)
