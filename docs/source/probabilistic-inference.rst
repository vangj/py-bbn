Probabilistic Inference
=======================

The probabilistic inference algorithm used by py-bbn is an exact inference algorithm. Let's go through
an example on how to conduct exact inference.

Huang Graph
-----------

Below is the code to create the `Huang Graph <http://pages.cs.wisc.edu/~dpage/ijar95.pdf>`_. Note the typical procedure as follows.

- create a Bayesian Belief Network (BBN)
- create a junction tree from the graph
- assert evidence
- print out the marginal probabilities

.. graphviz::
   :align: center
   :alt: Huang Bayesian Belief Network structure.
   :caption: Huang Bayesian Belief Network structure.

   digraph {
        node [fixedsize=true, width=0.3, shape=circle, fontname="Helvetica-Outline", color=crimson, style=filled]

        A -> B
        A -> C
        B -> D
        C -> E
        D -> F
        E -> F
        C -> G
        E -> H
        G -> H
   }

.. literalinclude:: code/create-huang-graph.py
   :language: python
   :linenos:

A Bayesian Belief Network (BBN) is defined as a pair, ``G, P``, where

- ``G`` is a directed acylic graph (DAG)
- ``P`` is a joint probability distribution
- and ``G`` satisfies the Markov Condition (nodes are conditionally independent of non-descendants given its parents)

Ideally, the API should force the user to define ``G`` and ``P`` separately. However, there will be a bit of ``cognitive friction``
with this API as we define nodes associated with their local probability models (conditional probability tables)
and then the structure afterwards. But this approach seems a bit more concise, no?

Updating Conditional Probability Tables
---------------------------------------

Sometimes, you may want to preserve the join tree structure and just update the condtional probability tables (CPTs).
Here's how to do so.

.. literalinclude:: code/updating-cpts.py
   :language: python
   :linenos:
   :emphasize-lines: 20

Note that we use ``InferenceController.reapply(...)`` to apply the new CPTs to a previous one and that we
get a new junction tree as an output.