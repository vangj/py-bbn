Causal Inference
================

Average Causal Effect
---------------------

Here's how you may estimate the Average Causal Effect ``ACE`` using Pearl's ``do-operator``.
In this example, we want to estimate the ACE of drug on recovery where recovery is true.

.. literalinclude:: code/ace-demo.py
   :language: python
   :linenos:
   :emphasize-lines: 29-33