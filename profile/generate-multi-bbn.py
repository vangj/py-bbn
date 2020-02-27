import json

import numpy as np

from pybbn.generator.bbngenerator import generate_multi_bbn, convert_for_exact_inference
from pybbn.graph.dag import Bbn

np.random.seed(37)

g, p = generate_multi_bbn(900, max_iter=10)
s_bbn = convert_for_exact_inference(g, p)

with open('multi-bbn.json', 'w') as f:
    f.write(json.dumps(Bbn.to_dict(s_bbn), sort_keys=True, indent=2))
