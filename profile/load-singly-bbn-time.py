import time

from pybbn.graph.dag import Bbn
from pybbn.pptc.inferencecontroller import InferenceController

# deserialization 0.02801
# junction tree 6.10584

start = time.time()

bbn = Bbn.from_json('singly-bbn.json')

stop = time.time()
diff = stop - start

print(f'deserialization {diff:.5f}')

start = time.time()

join_tree = InferenceController.apply(bbn)

stop = time.time()
diff = stop - start

print(f'junction tree {diff:.5f}')
