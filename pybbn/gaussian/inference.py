import numpy as np


class GaussianInference(object):
    def __init__(self, H, M, E):
        self.H = H
        self.M = M
        self.E = E
        self.I = {h: i for i, h in enumerate(H)}

    def do_inference(self, name, observation):
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

        return GaussianInference(H, M, E)

