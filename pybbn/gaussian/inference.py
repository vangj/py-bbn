import numpy as np


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

    @property
    def P(self):
        """
        Gets the univariate parameters of each variable.

        :return: Dictionary. Keys are variable names. Values are tuples of (mean, variance).
        """
        params = {k: (v, 0) for k, v in self.meta.items()}
        for i, (k, v) in enumerate(zip(self.H, self.M)):
            params[k] = (v, self.E[i][i])
        return params

    def do_inference(self, name, observation):
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

        :param name: Name of variable.
        :param observation: Observation value.
        :return: GaussianInference.
        """
        z_index = [self.I[name]]
        y_index = [i for i in range(self.E.shape[1]) if i not in z_index]

        m_Z = np.array([m for i, m in enumerate(self.M) if i in z_index])
        m_Y = np.array([m for i, m in enumerate(self.M) if i in y_index])

        z = np.array([observation])

        S_YZ = self.E[y_index][:, z_index]
        S_ZZ = np.linalg.inv(self.E[z_index][:, z_index])
        S_YY = self.E[y_index][:, y_index]

        H = [h for i, h in enumerate(self.H) if h != name]
        M = m_Y - S_YZ.dot(S_ZZ).dot(z - m_Z)
        E = S_YY - S_YZ.dot(S_ZZ).dot(S_YZ.T)
        meta = {**self.meta, **{name: observation}}

        return GaussianInference(H, M, E, meta)

    def get_inference(self, observations):
        """
        Conducts inference on a set of observations.

        :param observations: List of observation. Each observation is tuple (name, value).
        :return: GaussianInference.
        """
        o = observations[0]
        g = self.do_inference(o[0], o[1])
        for o in observations[1:]:
            g = g.do_inference(o[0], o[1])
        return g
