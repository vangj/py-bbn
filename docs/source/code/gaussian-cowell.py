import numpy as np

from pybbn.gaussian.inference import GaussianInference


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


# assume we have data and headers (variable names per column)
# X is the data (rows are observations, columns are variables)
# H is just a list of variable names
X, H = get_cowell_data()

# then we can compute the means and covariance matrix easily
M = X.mean(axis=0)
E = np.cov(X.T)

# the means and covariance matrix are all we need for gaussian inference
# notice how we keep `g` around?
# we'll use `g` over and over to do inference with evidence/observations
g = GaussianInference(H, M, E)
# {'Y': (0.00967, 0.98414), 'X': (0.01836, 2.02482), 'Z': (0.02373, 3.00646)}
print(g.P)

# we can make a single observation with do_inference()
g1 = g.do_inference('X', 1.5)
# {'X': (1.5, 0), 'Y': (0.76331, 0.49519), 'Z': (1.51893, 1.00406)}
print(g1.P)

# we can make multiple observations with do_inferences()
g2 = g.do_inferences([('Z', 1.5), ('X', 2.0)])
# {'Z': (1.5, 0), 'X': (2.0, 0), 'Y': (1.00770, 0.49509)}
print(g2.P)
