import time

from pybbn.graph.dag import Bbn
from pybbn.pptc.inferencecontroller import InferenceController

# deserialization 0.02502
# junction tree 19.76524

start = time.time()

bbn = Bbn.from_json('multi-bbn.json')

stop = time.time()
diff = stop - start

print(f'deserialization {diff:.5f}')

start = time.time()

join_tree = InferenceController.apply(bbn)

stop = time.time()
diff = stop - start

print(f'junction tree {diff:.5f}')
