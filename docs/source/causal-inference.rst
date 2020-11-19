Causal Inference
================

Average Causal Effect
---------------------

Here's how you may estimate the Average Causal Effect ``ACE`` using Pearl's ``do-operator``.
In this example, we want to estimate the ACE of drug on recovery where recovery is true.

.. graphviz::
   :align: center
   :alt: Z is confounding X and Y.
   :caption: Z is confounding X and Y.

   digraph {
        node [fixedsize=true, width=0.3, shape=circle, fontname="Helvetica-Outline", color=crimson, style=filled]

        Z -> X
        Z -> Y
        X -> Y
   }

.. literalinclude:: code/ace-demo.py
   :language: python
   :linenos:
   :emphasize-lines: 29-33