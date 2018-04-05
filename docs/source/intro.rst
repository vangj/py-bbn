Introduction
============

.. toctree::
   :maxdepth: 4

PyBBN is a very simple Python library for exact and approximate inference in Bayesian Belief Networks (BBNs). The exact inference algorithm is called the junction tree algorithm and used in this library only for BBNs having all discrete nodes/variables. The approximate inference algorithm is conducted using Gibbs sampling and used in this library only for BBNs having all continuous nodes/variables with the additional assumption of a multivariate Gaussian distribution.