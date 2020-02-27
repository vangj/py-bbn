import functools
import json
import timeit

from pybbn.graph.dag import Bbn
from pybbn.pptc.inferencecontroller import InferenceController


def do_it(bbn):
    InferenceController.apply(bbn)


with open('singly-bbn.json', 'r') as f:
    bbn = Bbn.from_dict(json.loads(f.read()))

    print('finished loading')

    n = 20
    t = timeit.Timer(functools.partial(do_it, bbn))
    d = t.timeit(n) / float(n)
    print(d)
