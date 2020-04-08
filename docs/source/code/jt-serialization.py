import json

from pybbn.graph.dag import Bbn
from pybbn.graph.edge import EdgeType, Edge
from pybbn.graph.jointree import JoinTree
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController

a = BbnNode(Variable(0, 'a', ['t', 'f']), [0.2, 0.8])
b = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
bbn = Bbn().add_node(a).add_node(b) \
    .add_edge(Edge(a, b, EdgeType.DIRECTED))
jt = InferenceController.apply(bbn)

with open('simple-join-tree.json', 'w') as f:
    d = JoinTree.to_dict(jt)
    j = json.dumps(d, sort_keys=True, indent=2)
    f.write(j)
