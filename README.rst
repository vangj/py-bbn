PyBBN
-----

PyBBN is Python library for Bayesian Belief Networks (BBNs) exact inference using the
`junction tree algorithm <https://en.wikipedia.org/wiki/Junction_tree_algorithm>`_ or Probability
Propagation in Trees of Clusters. The implementation is taken directly from `C. Huang and A. Darwiche, "Inference in
Belief Networks: A Procedural Guide," in International Journal of Approximate Reasoning, vol. 15,
pp. 225--263, 1999 <http://pages.cs.wisc.edu/~dpage/ijar95.pdf>`_. PyBBN also has approximate
inference algorithm using `Gibbs sampling <http://www.mit.edu/~ilkery/papers/GibbsSampling.pdf>`_ for
linear Gaussian BBN models. The exact inference algorithm is for BBNs that have all variables
that are discrete, while the approximate inference algorithm is for BBNs that have all variables
that are continuous (and assume to take a multivariate Gaussian distribution). Additionally, there is
the ability to generate singly- and multi-connected graphs, which is taken from `JS Ide and FG Cozman,
"Random Generation of Bayesian Network," in Advances in Artificial Intelligence, Lecture Notes in Computer Science, vol 2507 <https://pdfs.semanticscholar.org/5273/2fb57129443592024b0e7e46c2a1ec36639c.pdf>`_.

Exact Inference Usage
---------------------

Below is an example code to create a Bayesian Belief Network, transform it into a join tree,
and then set observation evidence. The last line prints the marginal probabilities for each node.

.. code:: python

    from pybbn.graph.dag import Bbn
    from pybbn.graph.edge import Edge, EdgeType
    from pybbn.graph.jointree import EvidenceBuilder
    from pybbn.graph.node import BbnNode
    from pybbn.graph.variable import Variable
    from pybbn.pptc.inferencecontroller import InferenceController

    # create the nodes
    a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
    b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
    c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])
    d = BbnNode(Variable(3, 'd', ['on', 'off']), [0.9, 0.1, 0.5, 0.5])
    e = BbnNode(Variable(4, 'e', ['on', 'off']), [0.3, 0.7, 0.6, 0.4])
    f = BbnNode(Variable(5, 'f', ['on', 'off']), [0.01, 0.99, 0.01, 0.99, 0.01, 0.99, 0.99, 0.01])
    g = BbnNode(Variable(6, 'g', ['on', 'off']), [0.8, 0.2, 0.1, 0.9])
    h = BbnNode(Variable(7, 'h', ['on', 'off']), [0.05, 0.95, 0.95, 0.05, 0.95, 0.05, 0.95, 0.05])

    # create the network structure
    bbn = Bbn() \
        .add_node(a) \
        .add_node(b) \
        .add_node(c) \
        .add_node(d) \
        .add_node(e) \
        .add_node(f) \
        .add_node(g) \
        .add_node(h) \
        .add_edge(Edge(a, b, EdgeType.DIRECTED)) \
        .add_edge(Edge(a, c, EdgeType.DIRECTED)) \
        .add_edge(Edge(b, d, EdgeType.DIRECTED)) \
        .add_edge(Edge(c, e, EdgeType.DIRECTED)) \
        .add_edge(Edge(d, f, EdgeType.DIRECTED)) \
        .add_edge(Edge(e, f, EdgeType.DIRECTED)) \
        .add_edge(Edge(c, g, EdgeType.DIRECTED)) \
        .add_edge(Edge(e, h, EdgeType.DIRECTED)) \
        .add_edge(Edge(g, h, EdgeType.DIRECTED))

    # convert the BBN to a join tree
    join_tree = InferenceController.apply(bbn)

    # insert an observation evidence
    ev = EvidenceBuilder() \
        .with_node(join_tree.get_bbn_node_by_name('a')) \
        .with_evidence('on', 1.0) \
        .build()
    join_tree.set_observation(ev)

    # print the marginal probabilities
    for node in join_tree.get_bbn_nodes():
        potential = join_tree.get_bbn_potential(node)
        print(node)
        print(potential)

Approximate Inference Usage
---------------------------

Below is an example to create a linear Gaussian BBN and perform inference.

.. code:: python

    import numpy as np
    from pybbn.lg.graph import Dag, Parameters, Bbn

    # create the directed acylic graph
    dag = Dag()
    dag.add_node(0)
    dag.add_node(1)
    dag.add_edge(0, 1)

    # create parameters
    means = np.array([0, 25])
    cov = np.array([
        [1.09, 1.95],
        [1.95, 4.52]
    ])
    params = Parameters(means, cov)

    # create the bayesian belief network
    bbn = Bbn(dag, params)

    # do the inference
    M, C = bbn.do_inference()
    print(M)

    # set the evidence on node 0 to a value of 1
    bbn.set_evidence(0, 1)
    M, C = bbn.do_inference()
    print(M)
    bbn.clear_evidences()

    # set the evidence on node 1 to a value of 20
    bbn.set_evidence(1, 20)
    M, C = bbn.do_inference()
    print(M)
    bbn.clear_evidences()

Building
--------

To build, you will need Python 2.7 or 3.7. Managing environments through `Anaconda <https://www.anaconda.com/download/#linux>`_
is highly recommended to be able to build this project (though not absolutely required if you know
what you are doing). Assuming you have installed Anaconda, you may create an environment as
follows (make sure you `cd` into the root of this project's location).

For Python 2.7.


.. code:: bash

    conda env create -f environment-py27.yml
    conda activate pybbn27
    python -m ipykernel install --user --name pybbn27 --display-name "pybbn27"


For Python 3.7.


.. code:: bash

    conda env create -f environment-py37.yml
    conda activate pybbn37
    python -m ipykernel install --user --name pybbn37 --display-name "pybbn37"


Then you may build the project as follows. (Note that in Python 3.6 you will get some warnings).


.. code:: bash

    make build


To build the documents, go into the docs sub-directory and type in the following.

.. code:: bash

    make html


Installing
----------

Use pip to install the package as it has been published to `PyPi <https://pypi.python.org/pypi/pybbn>`_.

.. code:: bash

    pip install pybbn


Other Python Bayesian Belief Network Inference Libraries
--------------------------------------------------------

Here is a list of other Python libraries for inference in Bayesian Belief Networks.

* `BayesPy <https://github.com/bayespy/bayespy>`_
* `pomegranate <https://github.com/jmschrei/pomegranate>`_
* `pgmpy <https://github.com/pgmpy/pgmpy>`_
* `libpgm <https://github.com/CyberPoint/libpgm>`_
* `bayesnetinference <https://github.com/sonph/bayesnetinference>`_

I found other `packages <https://pypi.python.org/pypi?%3Aaction=search&term=bayesian+network&submit=search>`_ in PyPI too.

Citation
--------

.. code::

    @misc{vang_2017,
    title={PyBBN},
    url={https://github.com/vangj/py-bbn/},
    journal={GitHub},
    author={Vang, Jee},
    year={2017},
    month={Jan}}


Copyright Stuff
---------------

.. code::

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
