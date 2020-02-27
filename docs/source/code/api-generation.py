import numpy as np

from pybbn.generator.bbngenerator import generate_bbn_to_file

# set the seed for reproducibility
np.random.seed(37)

# generate a singly-connected BBN
generate_bbn_to_file(n=10, file_path='singly-bbn.csv', bbn_type='singly', max_alpha=10)

# generate a multi-connected BBN
generate_bbn_to_file(n=10, file_path='multi-bbn.csv', bbn_type='multi', max_alpha=10)
