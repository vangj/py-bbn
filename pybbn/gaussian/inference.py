import numpy as np
import pandas as pd


class GaussianInference(object):
    """
    Gaussian inference.
    """

    def __init__(self, H, M, E, meta={}):
        """
        ctor.

        :param H: Headers.
        :param M: Means.
        :param E: Covariance matrix.
        :param meta: Dictionary storing observations.
        """
        self.H = H
        self.M = M
        self.E = E
        self.I = {h: i for i, h in enumerate(H)}
        self.meta = meta

    def __repr__(self):
        H = ','.join(self.H)
        M = ','.join([f'{m:.3f}' for m in self.M])
        E = '[' + '|'.join(['[' + ','.join([f'{self.E[r][c]:.3f}' for c in range(self.E.shape[1])]) + ']'
                            for r in range(self.E.shape[0])]) + ']'
        meta = '{' + ','.join([f'{k}={v:.3f}' for k, v in self.meta.items()]) + '}'
        s = f'GaussianInference[H=[{H}], M=[{M}], E={E}, meta={meta}]'
        return s

    def sample_marginals(self, size=1000):
        """
        Samples data from the marginals.

        :param size: Number of samples.
        :return: Dictionary with keys as names and values as pandas series (sampled data).
        """

        def get_samples(m, v):
            if v == 0.0:
                s = 0.01
            else:
                s = np.sqrt(v)
            return pd.Series(np.random.normal(m, s, size=size))

        return {m['name']: get_samples(m['mean'], m['var'])
                for m in self.marginals}

    @property
    def marginals(self):
        """
        Gets the marginals.

        :return: List of dictionary. Each element has name, mean and variance.
        """
        return [{'name': name, 'mean': mean, 'var': var}
                for name, (mean, var) in self.P.items()]

    @property
    def P(self):
        """
        Gets the univariate parameters of each variable.

        :return: Dictionary. Keys are variable names. Values are tuples of (mean, variance).
        """
        params = {k: (v, 0) for k, v in self.meta.items()}
        for i, (k, v) in enumerate(zip(self.H, self.M)):
            params[k] = (-v, self.E[i][i])
        return params

    def do_inference(self, name, observation):
        """
        Performs inference. Simply calls the `do_inferences` method.

        :param name: Name of variable.
        :param observation: Observation value.
        :return: GaussianInference.
        """
        return self.do_inferences([(name, observation)])

    def do_inferences(self, observations):
        """
        Performs inference.

        Denote the following.

        - :math:`z` as the variable observed
        - :math:`y` as the set of other variables
        - :math:`\\mu` as the vector of means
            - :math:`\\mu_z` as the partitioned :math:`\\mu`` of length :math:`|z|`
            - :math:`\\mu_y` as the partitioned :math:`\\mu`` of length :math:`|y|`
        - :math:`\\Sigma` as the covariance matrix
            - :math:`\\Sigma_{yz}` as the partitioned :math:`\\Sigma` of :math:`|y|` rows and :math:`|z|` columns
            - :math:`\\Sigma_{zz}` as the partitioned :math:`\\Sigma` of :math:`|z|` rows and :math:`|z|` columns
            - :math:`\\Sigma_{yy}` as the partitioned :math:`\\Sigma` of :math:`|y|` rows and :math:`|y|` columns

        If we observe evidence :math:`z_e`, then the new means :math:`\\mu_y^{*}` and
        covariance matrix :math:`\\Sigma_y^{*}` corresponding to :math:`y`
        are computed as follows.

        - :math:`\\mu_y^{*} = \\mu_y - \\Sigma_{yz} \\Sigma_{zz} (z_e - \\mu_z)`
        - :math:`\\Sigma_y^{*} = \\Sigma_{yy} \\Sigma_{zz} \\Sigma_{yz}^{T}`

        :param observations: List of observation. Each observation is tuple (name, value).
        :return: GaussianInference.
        """
        z_index = [self.I[name] for name, _ in observations]
        y_index = [i for i in range(self.E.shape[1]) if i not in z_index]

        m_Z = np.array([m for i, m in enumerate(self.M) if i in z_index])
        m_Y = np.array([m for i, m in enumerate(self.M) if i in y_index])

        z = np.array([o for _, o in observations])

        S_YZ = self.E[y_index][:, z_index]
        S_ZZ = np.linalg.inv(self.E[z_index][:, z_index])
        S_YY = self.E[y_index][:, y_index]

        H = [name for i, name in enumerate(self.H) if i in y_index]
        M = m_Y - S_YZ.dot(S_ZZ).dot(z - m_Z)
        E = S_YY - S_YZ.dot(S_ZZ).dot(S_YZ.T)
        meta = {**self.meta, **{n: o for n, o in observations}}

        return GaussianInference(H, M, E, meta)
