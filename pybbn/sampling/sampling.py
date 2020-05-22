import itertools
import bisect
import numpy as np
from collections import namedtuple
from functools import cmp_to_key
from numpy.random import uniform

SortableNode = namedtuple('SortableNode', 'node_id parent_ids')


class Table(object):
    def __init__(self, node, parents=[]):
        self.node = node
        self.parents = sorted(parents, key=lambda n: n.id)
        self.parent_ids = [p.id for p in parents]

        if len(parents) == 0:
            self.probs = np.array([node.probs]).cumsum()
        else:
            cartesian = itertools.product(*[node.variable.values for node in parents])
            get_kv = lambda i, v: f'{i}={v}'
            keys = [','.join([get_kv(node.id, val) for node, val in zip(parents, values)]) for values in cartesian]
            n = len(keys)

            probs = [node.probs[i:i + n] for i in range(0, len(node.probs), n)]
            probs = [np.array(p).cumsum() for p in probs]
            self.probs = {k: p for k, p in zip(keys, probs)}

    def get_value(self, prob, sample=None):
        if not self.has_parents():
            index = bisect.bisect(self.probs, prob)
        else:
            k = ','.join([f'{i}={sample[i]}' for i in self.parent_ids])
            probs = self.probs[k]
            index = bisect.bisect(probs, prob)
        return self.node.variable.values[index]

    def has_parents(self):
        return self.parents is not None and len(self.parents) > 0


class LogicSampler(object):
    """
    Logic sampling with rejection.
    """

    def __init__(self, bbn):
        """
        Ctor.
        :param bbn: BBN.
        """
        self.bbn = bbn
        self.nodes = self.__topological_sort__()
        self.tables = self.__get_tables__()

    def __get_tables__(self):
        tables = [node for node in self.bbn.get_nodes()]
        tables = [(node, self.bbn.get_parents_ordered(node.id)) for node in tables]
        tables = [(node, [self.bbn.get_node(pa_id) for pa_id in parents]) for node, parents in tables]
        tables = {node.id: Table(node, parents) for node, parents in tables}
        return tables

    def __topological_sort__(self):
        nodes = [SortableNode(node.id, set(self.bbn.get_parents_ordered(node.id))) for node in self.bbn.get_nodes()]
        id_sorter = lambda x, y: -1 if x < y else 1 if x > y else 0
        pa_sorter = lambda x, y: -1 if x.node_id in y.parent_ids else 1 if y.node_id in x.parent_ids else id_sorter(x.node_id, y.node_id)
        nodes = sorted(nodes, key=cmp_to_key(pa_sorter))
        nodes = [n.node_id for n in nodes]
        return nodes

    def get_samples(self, n_samples=100, seed=37):
        """
        Gets the samples.

        :param n_samples: Number of samples.
        :param seed: Seed (default=37).
        :return: Samples.
        """
        np.random.seed(seed)
        n = len(self.nodes)
        samples = []
        while True:
            sample = {}

            probs = uniform(0.0, 1.0, size=n)
            for p, node_id in zip(probs, self.nodes):
                table = self.tables[node_id]
                val = table.get_value(p, sample=sample)
                sample[node_id] = val

            samples.append(sample)

            if len(samples) == n_samples:
                break

        return samples
