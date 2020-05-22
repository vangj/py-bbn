import itertools
import bisect
import numpy as np


class Table(object):
    def __init__(self, node, parents=[]):
        self.node = node
        self.parents = sorted(parents, key=lambda n: n.id)

        if len(parents) == 0:
            self.probs = np.array([node.probs]).cumsum()
        else:
            cartesian = itertools.product(*[node.variable.values for node in parents])
            get_kv = lambda i, v: f'{i}={v}'
            keys = [','.join([get_kv(node.id, val) for node, val in zip(parents, values)]) for values in cartesian]
            n = len(keys)

            probs = [node.probs[i:i + n] for i in range(0, len(node.probs), n)]
            self.probs = {k: p for k, p in zip(keys, probs)}

    def has_parents(self):
        return self.parents is not None and len(self.parents) > 0


class LogicSampling(object):
    """
    Logic sampling with rejection.
    """

    def __init__(self, bbn):
        """
        Ctor.
        :param bbn: BBN.
        """
        self.bbn = bbn

    def __initialize__(self):
        def get_parents(n):
            return [self.bbn.get_node(pa_id) for pa_id in self.bbn.get_parents_ordered(n.id)]

        [[node] + get_parents(node) for node in self.bbn.get_nodes()]

    def get_samples(self, n_samples=100):
        """
        Gets the samples.

        :param n_samples: Number of samples.
        :return: Samples.
        """
        samples = []
        return samples
