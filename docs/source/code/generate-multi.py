import numpy as np

from pybbn.generator.bbngenerator import generate_multi_bbn, convert_for_exact_inference, convert_for_drawing

# very important to set the seed for reproducible results
np.random.seed(37)

# this method generates the graph, g, and probabilities, p
# note we are generating a multi-connected graph
g, p = generate_multi_bbn(5, max_iter=5)

# you have to convert g and p to a BBN
bbn = convert_for_exact_inference(g, p)

# you can convert the BBN to a nx graph for visualization
nx_graph = convert_for_drawing(bbn)
