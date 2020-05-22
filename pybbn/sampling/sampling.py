import bisect
import copy
import itertools
from functools import cmp_to_key

import numpy as np


class SortableNode(object):
    """
    Sortable node.
    """

    def __init__(self, node_id, parent_ids):
        """
        Ctor.

        :param node_id: Node ID.
        :param parent_ids: List of parent IDs.
        """
        self.node_id = node_id
        self.parent_ids = parent_ids


class Table(object):
    """
    Table association parent instantiations with cumulative distributions
    of node values.
    """

    def __init__(self, node, parents=[]):
        """
        Ctor.

        :param node: BBN node.
        :param parents: List of parent BBN nodes.
        """
        self.node = node
        self.parents = sorted(parents, key=lambda n: n.id)
        self.parent_ids = [p.id for p in parents]

        if len(parents) == 0:
            self.probs = np.array([node.probs]).cumsum()
        else:
            cartesian = list(itertools.product(*[node.variable.values for node in self.parents]))
            get_kv = lambda i, v: f'{i}={v}'
            keys = [','.join([get_kv(node.id, val) for node, val in zip(self.parents, values)]) for values in cartesian]
            n = len(node.variable.values)

            probs = [node.probs[i:i + n] for i in range(0, len(node.probs), n)]
            probs = [np.array(p).cumsum() for p in probs]
            self.probs = {k: p for k, p in zip(keys, probs)}

    def get_value(self, prob, sample=None):
        """
        Gets the value associated with the specified probability.

        :param prob: Probability.
        :param sample: Dictionary of variable-value sampled so far.
        :return: Value.
        """
        if not self.has_parents():
            index = bisect.bisect(self.probs, prob)
        else:
            k = ','.join([f'{i}={sample[i]}' for i in self.parent_ids])
            probs = self.probs[k]
            index = bisect.bisect(probs, prob)
        return self.node.variable.values[index]

    def has_parents(self):
        """
        Checks if the node associated with this table has parents.

        :return: Boolean.
        """
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
        """
        Gets a dictionary of node ID to Table.

        :return: Dictionary of node ID to Table.
        """
        tables = [node for node in self.bbn.get_nodes()]
        tables = [(node, self.bbn.get_parents_ordered(node.id)) for node in tables]
        tables = [(node, [self.bbn.get_node(pa_id) for pa_id in parents]) for node, parents in tables]
        tables = {node.id: Table(node, parents) for node, parents in tables}
        return tables

    def __topological_sort__(self):
        """
        Performs topological sort of nodes.

        :return: List of node IDs that is topologically sorted.
        """
        nodes = [SortableNode(node.id, set(self.bbn.get_parents_ordered(node.id))) for node in self.bbn.get_nodes()]
        id_sorter = lambda x, y: -1 if x < y else 1 if x > y else 0
        pa_sorter = lambda x, y: -1 if x.node_id in y.parent_ids else 1 if y.node_id in x.parent_ids else id_sorter(
            x.node_id, y.node_id)
        nodes = sorted(nodes, key=cmp_to_key(pa_sorter))
        nodes = [n.node_id for n in nodes]
        return nodes

    def get_samples(self, evidence={}, n_samples=100, seed=37):
        """
        Gets the samples.

        :param evidence: Evidence. Dictionary. Keys are ids and values are node values.
        :param n_samples: Number of samples.
        :param seed: Seed (default=37).
        :return: Samples.
        """
        np.random.seed(seed)
        n = len(self.nodes)
        samples = []
        while True:
            sample = copy.deepcopy(evidence)

            probs = np.random.uniform(0.0, 1.0, size=n)
            for p, node_id in zip(probs, self.nodes):
                table = self.tables[node_id]
                val = table.get_value(p, sample=sample)

                if node_id in evidence and val != evidence[node_id]:
                    break
                sample[node_id] = val

            if len(sample) == n:
                samples.append(sample)

            if len(samples) == n_samples:
                break

        return samples
