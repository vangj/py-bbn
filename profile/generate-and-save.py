import numpy as np

from pybbn.generator.bbngenerator import generate_bbn_to_file
from pybbn.graph.dag import BbnUtil, Bbn

np.random.seed(37)

generate_bbn_to_file(900, 'singly-bbn.csv', 'singly', 10)
generate_bbn_to_file(900, 'multi-bbn.csv', 'multi', 10)

bbn = BbnUtil.get_huang_graph()
Bbn.to_csv(bbn, 'huang.csv')
