Generating Bayesian Belief Networks
===================================

Let's generate some Bayesian Belief Networks (BBNs). The algorithms are taken from `Random Generation of Bayesian Networks <https://www.semanticscholar.org/paper/Random-Generation-of-Bayesian-Networks-Ide-Cozman/52732fb57129443592024b0e7e46c2a1ec36639c>`_.
There are two types of BBNs you may generate.

- singly-connected
- multi-connected

A singly-connected BBN is one, where ignoring the direction of the edges, there is at most one path between any two nodes.
A multi-connected BBN is one that is ``not`` singly-connected.

Singly-Connected
----------------

The key method to use here is ``generate_singly_bbn``.

.. literalinclude:: code/generate-singly.py
   :language: python
   :linenos:
   :emphasize-lines: 10


Multi-Connected
---------------

The key method to use here is ``generate_multi_bbn``.

.. literalinclude:: code/generate-multi.py
   :language: python
   :linenos:
   :emphasize-lines: 10

Direct Generation
-----------------

In the case where you do ``NOT`` need a reference to the BBN objects, use the API's convenience method to generate and serialize the BBN directly to file.

.. literalinclude:: code/api-generation.py
   :language: python
   :linenos:
   :emphasize-lines: 9, 12

Here's the output for ``singly-bbn.csv``.

.. literalinclude:: code/singly-bbn.csv
   :language: text
   :linenos:

Here's the output for ``multi-bbn.csv``.

.. literalinclude:: code/multi-bbn.csv
   :language: text
   :linenos: