Sampling Data
=============

Sampling data from a BBN is possible. The algorithm uses ``logic sampling with rejection``.

Simple Sampling
---------------

This code demonstrates simple sampling.

.. literalinclude:: code/logic-sampling.py
   :language: python
   :linenos:
   :emphasize-lines: 18-19


Sampling with Rejection
-----------------------

This code demonstrates sampling with evidence asserted. During each round of sampling, if the sample
value generated does not match with the evidence, the entire sample is discarded.

.. literalinclude:: code/logic-sampling-rejection.py
   :language: python
   :linenos:
   :emphasize-lines: 18-19
