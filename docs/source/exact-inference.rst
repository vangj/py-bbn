Exact Inference
===============

Huang Graph
-----------

Below is the code to create the Huang Graph. Note the typical procedure as follows.

- create a Bayesian Belief Network (BBN)
- create a junction tree from the graph
- assert evidence
- print out the marginal probabilities

.. literalinclude:: code/create-huang-graph.py
   :language: python
   :linenos:

Updating Conditional Probability Tables
---------------------------------------

Sometimes, you may want to preserve the join tree structure and just update the condtional probability tables (CPTs).
Here's how to do so.

.. literalinclude:: code/updating-cpts.py
   :language: python
   :linenos:

