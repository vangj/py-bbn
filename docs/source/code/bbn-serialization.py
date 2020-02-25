import json

from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.lg.graph import Bbn

# create graph
a = BbnNode(Variable(0, 'a', ['t', 'f']), [0.2, 0.8])
b = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
bbn = Bbn().add_node(a).add_node(b) \
    .add_edge(Edge(a, b, EdgeType.DIRECTED))

# serialize to JSON file
s = json.dumps(Bbn.to_dict(bbn))
with open('simple-bbn.json', 'w') as f:
    f.write(s)
