# PyBBN

PyBBN is Python library for Bayesian Belief Networks (BBNs) exact inference using the 
[junction tree algorithm](https://en.wikipedia.org/wiki/Junction_tree_algorithm) or Probability
Propagation in Trees of Clusters. The implementation is taken directly from [C. Huang and A. Darwiche, "Inference in
Belief Networks: A Procedural Guide," in International Journal of Approximate Reasoning, vol. 15,
pp. 225--263, 1999](http://pages.cs.wisc.edu/~dpage/ijar95.pdf). PyBBN also has approximate
inference algorithm using [Gibbs sampling](http://www.mit.edu/~ilkery/papers/GibbsSampling.pdf) for
linear Gaussian BBN models. The exact inference algorithm is for BBNs that have all variables
that are discrete, while the approximate inference algorithm is for BBNs that have all variables
that are continuous (and assume to take a multivariate Gaussian distribution).

# Exact Inference Usage

Below is an example code to create a Bayesian Belief Network, transform it into a join tree, 
and then set observation evidence. The last line prints the marginal probabilities for each node.

```python
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
```

# Approximate Inference Usage

Below is an example to create a linear Gaussian BBN and perform inference.

```python
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
bbn = Bbn(dag, params, max_samples=2000, max_iters=10)

# do the inference
s = bbn.do_inference()
print(s)

# set the evidence on node 0 to a value of 1
bbn.set_evidence(0, 1)
s = bbn.do_inference()
print(s)
bbn.clear_evidences()

# set the evidence on node 1 to a value of 20
bbn.set_evidence(1, 20)
s = bbn.do_inference()
print(s)
bbn.clear_evidences()
```

# Building

To build, you will need Python 2.7+. Managing environments through [Anaconda](https://www.anaconda.com/download/#linux)
is highly recommended to be able to build this project (though not absolutely required if you know
what you are doing). Assuming you have installed Anaconda, you may create an environment as
follows (make sure you `cd` into the root of this project's location).

```bash
conda create -n py-bbn python=2.7
source activate py-bbn
conda install --yes --file requirements.txt
```

Then you may build the project as follows.

```
make build
```

To build the documents, go into the docs sub-directory and type in the following.

```
make html
```

# Installing

Use pip to install the package as it has been published to [PyPi](https://pypi.python.org/pypi/pybbn).

```bash
pip install pybbn
```

# Other Python Bayesian Belief Network Inference Libraries

Here is a list of other Python libraries for inference in Bayesian Belief Networks. 

| Library | Algorithm | Algorithm Type | License |
| -------:| ---------:| -------------: | -------:|
| [BayesPy](https://github.com/bayespy/bayespy)| variational message passing | approximate | MIT |
| [pomegranate](https://github.com/jmschrei/pomegranate) | loopy belief | approximate | MIT |
| [pgmpy](https://github.com/pgmpy/pgmpy) | multiple | approximate/exact | MIT |
| [libpgm](https://github.com/CyberPoint/libpgm) | likelihood sampling | approximate | Proprietary |
| [bayesnetinference](https://github.com/sonph/bayesnetinference) | variable elimination | exact | None |

I found other [packages](https://pypi.python.org/pypi?%3Aaction=search&term=bayesian+network&submit=search) in PyPI too.
