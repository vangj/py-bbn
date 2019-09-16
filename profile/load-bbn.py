import json

from pybbn.graph.dag import Bbn
from pybbn.pptc.inferencecontroller import InferenceController

with open('singly-bbn.json', 'r') as f:
    bbn = Bbn.from_dict(json.loads(f.read()))

print('finished loading')

join_tree = InferenceController.apply(bbn)
for node in join_tree.get_bbn_nodes():
    potential = join_tree.get_bbn_potential(node)
    print(node)
    print(potential)
    print('>')
