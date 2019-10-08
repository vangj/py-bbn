import json
import time

from pybbn.graph.dag import Bbn
from pybbn.pptc.inferencecontroller import InferenceController


def do_it(join_tree):
    InferenceController.reapply(join_tree, {0: [0.5, 0.5]})


with open('singly-bbn.json', 'r') as f:
    s = time.time()
    bbn = Bbn.from_dict(json.loads(f.read()))
    e = time.time()
    d = e - s
    print('{:.5f} seconds to load'.format(d))

    s = time.time()
    join_tree = InferenceController.apply(bbn)
    e = time.time()
    d = e - s
    print('{:.5f} seconds to create join tree'.format(d))

    InferenceController.reapply(join_tree, {0: [0.5, 0.5]})
