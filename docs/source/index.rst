.. meta::
   :description: An exact probabilistic and causal inference API using Bayesian Belief Networks (BBNs).
   :keywords: python, statistics, causal, causality, probabilistic, exact inference, bayesian, bayesian belief networks, logic sampling, sampling, graph, synthetic data
   :robots: index, follow
   :abstract: Exact probabilistic inference is accomplished using the Junction Tree Algorithm. Causal inference is accomplished using the average causal effect (ACE). Simulation features for generating synthetic data is also available. Feature to generate synthetic BBNs is also built in. Comes with batteries for experimentation and production-ready use.
   :author: Jee Vang
   :contact: vangjee@gmail.com
   :copyright: Jee Vang
   :content: global
   :generator: Sphinx
   :language: English
   :rating: general
   :reply-to: vangjee@gmail.com
   :web_author: Jee Vang
   :revisit-after: 1 days

.. PyBBN documentation master file, created by
   sphinx-quickstart on Tue Jan 17 17:44:12 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

py-bbn
======

.. graphviz::
   :align: center
   :alt: Converging network structure.

   digraph {
      node [shape=circle, fontname="Helvetica-Outline"]
      A [color=crimson, style=filled]
      B [color=crimson, style=filled]
      C [color=crimson, style=filled]

      A -> B
      C -> B
   }

``py-bbn`` is a Python implementation of exact inference in Bayesian Belief Networks. If you like py-bbn,
you might be interested in our next-generation products. Please contact us at info@oneoffcoder.com. Let's
reach for success!

* `turing_bbn <https://turing-bbn.oneoffcoder.com/>`_ is a C++17 implementation of py-bbn; take your causal and probabilistic inferences to the next computing level!
* `pyspark-bbn <https://pyspark-bbn.oneoffcoder.com/>`_ is a is a scalable, massively parallel processing MPP framework for learning structures and parameters of Bayesian Belief Networks BBNs using `Apache Spark <https://spark.apache.org/>`_.


.. toctree::
   :maxdepth: 2
   :caption: Contents

   intro
   probabilistic-inference
   causal-inference
   serde
   generate
   sampling


.. toctree::
   :maxdepth: 2
   :caption: API Documentation

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
