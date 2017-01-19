# PyBBN

PyBBN is Python library for Bayesian Belief Networks (BBNs) exact inference using the 
[junction tree algorithm](https://en.wikipedia.org/wiki/Junction_tree_algorithm) or Probability
Propagation in Trees of Clusters. The implementation is taken directly from [C. Huang and A. Darwiche, "Inference in
Belief Networks: A Procedural Guide," in International Journal of Approximate Reasoning, vol. 15,
pp. 225--263, 1999](http://pages.cs.wisc.edu/~dpage/ijar95.pdf).

# Usage

Below is an example code to create a Bayesian Belief Network, transform it into a join tree, 
and then set observation evidence. The last line prints the marginal probabilities for each node.

```python
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
bbn = Bbn()\
    .add_node(a)\
    .add_node(b)\
    .add_node(c)\
    .add_node(d)\
    .add_node(e)\
    .add_node(f)\
    .add_node(g)\
    .add_node(h)\
    .add_edge(Edge(a, b, EdgeType.DIRECTED))\
    .add_edge(Edge(a, c, EdgeType.DIRECTED))\
    .add_edge(Edge(b, d, EdgeType.DIRECTED))\
    .add_edge(Edge(c, e, EdgeType.DIRECTED))\
    .add_edge(Edge(d, f, EdgeType.DIRECTED))\
    .add_edge(Edge(e, f, EdgeType.DIRECTED))\
    .add_edge(Edge(c, g, EdgeType.DIRECTED))\
    .add_edge(Edge(e, h, EdgeType.DIRECTED))\
    .add_edge(Edge(g, h, EdgeType.DIRECTED))

# convert the BBN to a join tree
join_tree = InferenceController.apply(bbn)

# insert an observation evidence
ev = EvidenceBuilder()\
    .with_node(join_tree.get_bbn_node_by_name('a'))\
    .with_evidence('on', 1.0)\
    .build()
join_tree.set_observation(ev)

# print the marginal probabilities
for node in join_tree.get_bbn_nodes():
    potential = join_tree.get_bbn_potential(node)
    print(node)
    print(potential)

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
