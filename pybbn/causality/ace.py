import itertools
import operator
from functools import reduce

from pybbn.graph.jointree import EvidenceBuilder
from pybbn.pptc.inferencecontroller import InferenceController


class Ace(object):
    """
    Estimates average causal effect (ACE).
    """

    def __init__(self, bbn):
        """
        ctor

        :param bbn: Bayesian belief network.
        """
        self.bbn = bbn
        self.jt = InferenceController.apply(bbn)

    def get_ace(self, x, y, y_val):
        """
        Computes the ACE of X on Y.

        :param x: X name.
        :param y: Y name.
        :param y_val: Y value.
        :return: Dictionary of ACE over X values.
        """

        def get_evidence(n, v):
            return EvidenceBuilder() \
                .with_node(self.jt.get_bbn_node_by_name(n)) \
                .with_evidence(v, 1.0) \
                .build()

        def get_evidences(Z):
            return [get_evidence(n, v) for n, v in Z]

        def get_y_xz_prob(x, z):
            evs = [x] + z
            self.jt.unobserve_all()
            self.jt.update_evidences(evs)
            posteriors = self.jt.get_posteriors()
            return posteriors[y][y_val]

        def get_z_prob(z):
            self.jt.unobserve_all()
            posteriors = self.jt.get_posteriors()
            probs = [posteriors[n][v] for n, v in z]
            probs = reduce(operator.mul, probs, 1)
            return probs

        n2i = self.bbn.get_n2i()
        i2n = self.bbn.get_i2n()

        Z = self.bbn.get_parents(n2i[x])
        Z_names = [i2n[z] for z in Z]
        Z_values = list(itertools.product(*[self.bbn.get_node(z).variable.values for z in Z]))
        Z_values = [[(z, v) for z, v in zip(Z_names, tup)] for tup in Z_values]
        x_values = [(x, v) for v in self.bbn.get_node(n2i[x]).variable.values]

        results = {}
        for x_name, x_val in x_values:
            total = 0.0
            x_ev = get_evidence(x_name, x_val)
            for z in Z_values:
                z_ev = get_evidences(z)
                p_y_xz = get_y_xz_prob(x_ev, z_ev)
                p_z = get_z_prob(z)
                p = p_y_xz * p_z
                total += p

            results[x_val] = total

        return results
