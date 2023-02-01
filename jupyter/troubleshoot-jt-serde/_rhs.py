from pybbn.graph.jointree import JoinTree
from pybbn.pptc.inferencecontroller import InferenceController
import json

with open('./_tmp/join-tree.json', 'r') as f:
    j = f.read()
    d = json.loads(j)
    jt = JoinTree.from_dict(d)
    jt = InferenceController.apply_from_serde(jt)

print('done')
