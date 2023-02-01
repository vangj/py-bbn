from pybbn.graph.dag import Bbn
from pybbn.pptc.inferencecontroller import InferenceController

bbn = Bbn.from_json('./_tmp/covid-bbn.json')
jt = InferenceController.apply(bbn)

print('done')
