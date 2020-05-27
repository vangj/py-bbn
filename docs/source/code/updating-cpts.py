from pybbn.graph.dag import Bbn
from pybbn.graph.edge import EdgeType, Edge
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController

# you have built a BBN
a = BbnNode(Variable(0, 'a', ['t', 'f']), [0.2, 0.8])
b = BbnNode(Variable(1, 'b', ['t', 'f']), [0.1, 0.9, 0.9, 0.1])
bbn = Bbn().add_node(a).add_node(b) \
    .add_edge(Edge(a, b, EdgeType.DIRECTED))

# you have built a junction tree from the BBN
# let's call this "original" junction tree the left-hand side (lhs) junction tree
lhs_jt = InferenceController.apply(bbn)

# you may just update the CPTs with the original junction tree structure
# the algorithm to find/build the junction tree is avoided
# the CPTs are updated
rhs_jt = InferenceController.reapply(lhs_jt, {0: [0.3, 0.7], 1: [0.2, 0.8, 0.8, 0.2]})

# let's print out the marginal probabilities and see how things changed
# print the marginal probabilities for the lhs junction tree
print('lhs probabilities')
# print the posterior probabilities
for node, posteriors in lhs_jt.get_posteriors().items():
    p = ', '.join([f'{val}={prob:.5f}' for val, prob in posteriors.items()])
    print(f'{node} : {p}')

# print the marginal probabilities for the rhs junction tree
print('rhs probabilities')
for node, posteriors in rhs_jt.get_posteriors().items():
    p = ', '.join([f'{val}={prob:.5f}' for val, prob in posteriors.items()])
    print(f'{node} : {p}')
