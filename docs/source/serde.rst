Serialization/Deserialization
=============================

We all need a way to save (serialize) and load (deserialize) our Bayesian Belief Networks (BBNs) and join trees (JTs).
Here's how to do so. Note that serde (serialization/deserialization) features are just writing to JSON or CSV formats and
loading back from the such files. The code takes care of the serde process.

Serializing a BBN
-----------------

JSON Serialization Format
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: code/bbn-json-serialization.py
   :language: python
   :linenos:

You will get a file ``simple-bbn.json`` written out with the following content.

.. literalinclude:: code/simple-bbn.json
   :language: json
   :linenos:

CSV Serialization Format
^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: code/bbn-csv-serialization.py
   :language: python
   :linenos:

You will get a file ``simple-bbn.csv`` written out with the following content.

.. literalinclude:: code/simple-bbn.csv
   :language: text
   :linenos:

Deserializing a BBN
-------------------

JSON Deserialization Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: code/bbn-json-deserialization.py
   :language: python
   :linenos:

CSV Deserialization Format
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: code/bbn-csv-deserialization.py
   :language: python
   :linenos:

Join Tree Serde
---------------

A join tree may also be serialized and deserialized. Only ``json`` format is supported for now.

Serializing a Join Tree
^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: code/jt-serialization.py
   :language: python
   :linenos:

You will get a file ``simple-join-tree.json`` written out with the following content.

.. literalinclude:: code/simple-join-tree.json
   :language: json
   :linenos:

Deserializing a Join Tree
^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: code/jt-deserialization.py
   :language: python
   :linenos: