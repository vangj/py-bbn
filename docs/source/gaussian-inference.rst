Gaussian Inference
==================

Inference on a Gaussian Bayesian Network (GBN) is accomplished through updating the means and covariance matrix incrementally.

.. graphviz::
   :align: center
   :alt: Cowell GBN structure.
   :caption: Cowell GBN structure.

   digraph {
        node [fixedsize=true, width=0.3, shape=circle, fontname="Helvetica-Outline", color=crimson, style=filled]

        Y -> X
        X -> Z
   }

The variables come from the following Gaussian distributions.

- :math:`Y = \mathcal{N}(0, 1)`
- :math:`X = \mathcal{N}(Y, 1)`
- :math:`Z = \mathcal{N}(Z, 1)`

Below is a code sample of how we can perform inference on this GBN.

.. literalinclude:: code/gaussian-cowell.py
   :language: python
   :linenos: