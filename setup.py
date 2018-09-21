from setuptools import setup, find_packages

setup(
    name='pybbn',
    version='0.0.6',
    author='Jee Vang',
    author_email='vangjee@gmail.com',
    packages=find_packages(),
    description='Inference in Bayesian Belief Networks using Probability Propagation in Trees of Clusters (PPTC) and Gibbs sampling',
    url='https://github.com/vangj/py-bbn',
    keywords=['bayesian', 'belief', 'network', 'exact', 'approximate', 'inference', 'junction', 'tree', 'algorithm',
              'pptc', 'dag', 'gibbs', 'sampling', 'multivariate', 'conditional', 'gaussian', 'linear'],
    classifiers=[]
)
