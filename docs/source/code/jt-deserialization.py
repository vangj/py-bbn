import json

from pybbn.graph.jointree import JoinTree
from pybbn.pptc.inferencecontroller import InferenceController

with open('simple-join-tree.json', 'r') as f:
    j = f.read()
    d = json.loads(j)
    jt = JoinTree.from_dict(d)
    jt = InferenceController.apply_from_serde(jt)
