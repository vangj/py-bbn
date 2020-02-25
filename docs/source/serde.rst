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

You will get a file ``simple-bbn.json`` written out with the following content.

.. literalinclude:: code/simple-bbn.json
   :language: json
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

You will get a file ``simple-join-tree.json`` written out with the following content.

.. literalinclude:: code/simple-join-tree.json
   :language: json
   :linenos:

Deserializing a Join Tree
-------------------------

.. literalinclude:: code/jt-deserialization.py
   :language: python
   :linenos: