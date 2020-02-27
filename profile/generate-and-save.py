import numpy as np

from pybbn.generator.bbngenerator import generate_bbn_to_file

np.random.seed(37)

generate_bbn_to_file(900, 'singly-bbn.csv', 'singly', 10)
generate_bbn_to_file(900, 'multi-bbn.csv', 'multi', 10)
