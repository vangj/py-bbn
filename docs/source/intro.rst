Introduction
============

``py-bbn`` is a very simple Python library for exact and approximate inference in Bayesian Belief Networks (BBNs).
The exact inference algorithm is called the junction tree algorithm and used in this library only for BBNs
having all discrete nodes/variables. Additional feature includes generating singly- and multi-connected BBNs
so that you may use these generated BBNs for research purposes. There is also the option to generate sample
data from your BBN. This synthetic data may be summarized to generate your posterior marginal probabilities
and work as a form of approximate inference.

Source Code
-----------

Full source code is available on `GitHub <https://github.com/vangj/py-bbn>`_.

PyPi
----

You may install ``py-bbn`` from `pypi <https://pypi.org/project/pybbn/>`_.

.. code:: bash

    pip install pybbn

Copyright
---------

Boring Copyright Stuff::

    Copyright 2017 Jee Vang

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Citation
--------

Cite this project as follows::

    @misc{vang_2017,
    title={PyBBN},
    url={https://github.com/vangj/py-bbn/},
    journal={GitHub},
    author={Vang, Jee},
    year={2017},
    month={Jan}}
