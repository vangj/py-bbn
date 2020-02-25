Serialization/Deserialization
=============================

We all need a way to save (serialize) and load (deserialize) our Bayesian Belief Networks (BBNs) and join trees (JTs).
Here's how to do so. Note that serde (serialization/deserialization) features are just writing to JSON format and
loading back from the JSON. The code takes care of the serde process.

Serializing a BBN
-----------------

.. literalinclude:: code/bbn-serialization.py
   :language: python
   :linenos:

Deserializing a BBN
-------------------

.. literalinclude:: code/bbn-deserialization.py
   :language: python
   :linenos:

Serializing a Join Tree
-----------------------

.. literalinclude:: code/jt-serialization.py
   :language: python
   :linenos:

Deserializing a Join Tree
-------------------------

.. literalinclude:: code/jt-deserialization.py
   :language: python
   :linenos: