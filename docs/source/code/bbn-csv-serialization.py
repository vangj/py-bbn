from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable

# create graph
a = BbnNode(Variable(0, 'a', ['t', 'f']), [0.2, 0.8])
b = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
bbn = Bbn().add_node(a).add_node(b) \
    .add_edge(Edge(a, b, EdgeType.DIRECTED))

# serialize
Bbn.to_csv(bbn, 'simple-bbn.csv')
