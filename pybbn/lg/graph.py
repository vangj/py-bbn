import math
from collections import namedtuple

import networkx as nx
import numpy as np
from joblib import Parallel, delayed
from networkx.algorithms.dag import topological_sort, is_directed_acyclic_graph
from scipy.stats import multivariate_normal

from pybbn.lg.gaussian import dnorm, dcmvnorm
from pybbn.lg.inference import MvnInference

WORK_UNIT = namedtuple('WORK_UNIT', 'row_id node_id m s dep')
WORK_UNITS = namedtuple('WORK_UNITS', 'row_id units')
WORK_RESULT = namedtuple('WORK_RESULT', 'row_id, prob')


def __get__prob__(X, W):
    if W.dep is None:
        d = [X[W.row_id, W.node_id]]
        return next(dnorm(d, W.m, W.s))
    else:
        d = X[W.row_id, :].reshape(1, -1)
        return next(dcmvnorm(d, W.m, W.s, W.node_id, W.dep))


def __get_probs__(X, W):
    probs = [__get__prob__(X, w) for w in W.units]
    prob = 10 ** np.log10(probs).sum()
    return WORK_RESULT(W.row_id, prob)


def __get_log_prob__(X, W):
    if W.dep is None:
        d = [X[W.row_id, W.node_id]]
        return np.log10(next(dnorm(d, W.m, W.s)))
    else:
        d = X[W.row_id, :].reshape(1, -1)
        return np.log10(next(dcmvnorm(d, W.m, W.s, W.node_id, W.dep)))


def __get_log_probs__(X, W):
    p = np.sum([__get_log_prob__(X, w) for w in W.units])
    return WORK_RESULT(W.row_id, p)


class Dag(object):
    """
    Directed acyclic graph.
    """

    def __init__(self):
        """
        Ctor.
        """
        self.g = nx.DiGraph()

    def add_node(self, node_id, metadata={}):
        """
        Adds a node.

        :param node_id: Node ID.
        :param metadata: Metadata (JSON-like).
        :return: DAG.
        """
        self.g.add_node(node_id, metadata=metadata)
        return self

    def add_edge(self, parent_id, child_id, metadata={}):
        """
        Adds an edge.

        :param parent_id: Parent node ID.
        :param child_id: Child node ID.
        :param metadata: Metadata (JSON-like).
        :return: DAG.
        """
        self.g.add_edges_from([(parent_id, child_id, metadata)])
        if is_directed_acyclic_graph(self.g) is False:
            self.g.remove_edge(parent_id, child_id)
            raise ValueError('adding link from parent {} to child {} will create a cycle'.format(parent_id, child_id))
        return self

    def nodes(self):
        """
        Gets a list of all the node IDs.

        :return: List of node IDs.
        """
        return list(self.g.nodes())

    def edges(self):
        """
        Gets a list of all the edges.

        :return: List of edges.
        """
        return list(self.g.edges())

    def number_of_nodes(self):
        """
        Gets the number of nodes.

        :return: Number of nodes.
        """
        return self.g.number_of_nodes()

    def number_of_edges(self):
        """
        Gets the number of edges.

        :return: Number of edges.
        """
        return self.g.number_of_edges()

    def parents(self, node_id):
        """
        Gets the parents for the specified node ID.

        :param node_id: Node ID.
        :return: List of parent node IDs.
        """
        return list(self.g.predecessors(node_id))

    def children(self, node_id):
        """
        Gets the children for the specified node ID.

        :param node_id: Node ID.
        :return: List of children node IDs.
        """
        return list(self.g.successors(node_id))

    def coparents(self, node_id):
        """
        Gets the coparents of the specified node.

        :param node_id:  Node ID.
        :return: List of coparent node IDS.
        """
        copas = set()
        for ch in self.children(node_id):
            pas = self.parents(ch)
            for pa in pas:
                copas.add(pa)
        return list(copas)

    def markov_blanket(self, node_id):
        """
        Gets the Markov blanket of the specified node. The Markov blanket of a node is defined as its parents,
        children, and co-parents.

        :param node_id: Node ID.
        :return: List of node IDs in the Markov blanket.
        """
        blanket = set()

        for pa in self.parents(node_id):
            blanket.add(pa)
        for ch in self.children(node_id):
            blanket.add(ch)
        for copa in self.coparents(node_id):
            blanket.add(copa)

        if node_id in blanket:
            blanket.remove(node_id)
        return sorted(list(blanket))

    def get_sorted_topology(self):
        """
        Gets the sorted topology of the DAG.

        :return: Sorted topology of the DAG.
        """
        return list(topological_sort(self.g))


class Parameters(object):
    """
    Parameters, which are made up of the means and covariance matrix.
    """

    def __init__(self, means, cov):
        """
        Ctor.

        :param means: Means.
        :param cov: Covariance matrix.
        """
        self.means = means
        self.cov = cov

        if len(means) != cov.shape[0]:
            raise ValueError('number of means {} != number of variables {}'.format(len(means), cov.shape[0]))
        if cov.shape[0] != cov.shape[1]:
            raise ValueError('covariance matrix is not square: {} x {}'.format(cov.shape[0], cov.shape[1]))

    def get_mean(self, node_id):
        """
        Gets the mean associated with the node ID.

        :param node_id: Integer node ID.
        :return: Mean.
        """
        return self.means[node_id]

    def get_stdev(self, node_id):
        """
        Gets the standard deviation associated with the node ID.

        :param node_id: Integer node ID.
        :return: Variance.
        """
        return np.sqrt(self.cov[node_id, node_id])


class Bbn(object):
    """
    Bayesian Belief Network.
    """

    def __init__(self, dag, params):
        """
        Ctor. Note that the dimensions of the DAG and parameters must match.

        :param dag: DAG.
        :param params: Parameters (means and covariance).
        """
        self.dag = dag
        self.params = params
        self.mvn = MvnInference(params.means, params.cov)
        self.evidence = [None for _ in range(dag.number_of_nodes())]

        # all of these checks are to make sure the DAG and params align
        # check for 1-to-1 correspondence between nodes and variables
        num_nodes = dag.number_of_nodes()
        num_means = len(params.means)
        dag_nodes = dag.nodes()
        min_node_id = min(dag_nodes)
        max_node_id = max(dag_nodes)

        # num_vars1 = params.cov.shape[0]
        # num_vars2 = params.cov.shape[1]

        if num_nodes != num_means:
            raise ValueError('number of nodes {} != number of means {}'.format(num_nodes, num_means))
        # if num_nodes != num_vars1:
        #     raise ValueError('number of nodes {} != number of variables {}'.format(num_nodes, num_vars1))
        # if num_vars1 != num_vars2:
        #     raise ValueError('covariance is not a square; rows = {}, cols = {}'.format(num_vars1, num_vars2))
        if 0 != min_node_id:
            raise ValueError('Node IDs should start with zero, but it started with {}'.format(min_node_id))
        if num_nodes - 1 != max_node_id:
            raise ValueError('Node IDs should end with number_of_nodes - 1, but it was {}'.format(max_node_id))

        # make sure the node IDs are sequential
        for e, o in zip(range(num_nodes), sorted(dag_nodes)):
            if e != o:
                raise ValueError('Node IDs should be sequential integers but was not: {}'.format(sorted(dag.nodes())))

    def set_evidence(self, node_id, e):
        """
        Sets the evidence for the specified node.

        :param node_id: Node ID.
        :param e: Evidence.
        :return: BBN.
        """
        self.evidence[node_id] = e
        return self

    def get_evidence(self, node_id):
        """
        Gets the evidence for the specified node.

        :param node_id: Node ID.
        :return: Evidence.
        """
        return self.evidence[node_id]

    def get_evidences(self):
        """
        Gets all the evidences.

        :return: Array of evidences.
        """
        return self.evidence

    def clear_evidences(self):
        """
        Clears all the evidences.

        :return: None
        """
        self.evidence = [None for _ in range(self.dag.number_of_nodes())]

    def __has_parents__(self, node_id):
        """
        Checks if the specified node has parents.

        :param node_id: Node ID.
        :return: A boolean indicating if the node has parents.
        """
        return len(self.dag.parents(node_id)) > 0

    def __has_evidence__(self, node_id):
        """
        Checks if the specified node has evidence.

        :param node_id: Node ID.
        :return: A boolean indicating if the node has evidence.
        """
        return False if np.isnan(self.evidence[node_id]) else True

    def __get_evidences__(self):
        evidences = [(i, v) for i, v in enumerate(self.evidence)]
        evidences = list(filter(lambda tup: tup[1] is not None, evidences))
        v = list(map(lambda tup: tup[1], evidences))
        iv = list(map(lambda tup: tup[0], evidences))
        return v, iv

    def do_inference(self, N=None):
        """
        Conducts inference.

        :param N: Number of samples. If an integer is provided, the sampled means and covariances will be returned.
        :return: (means, covariances)
        """
        v, iv = self.__get_evidences__()
        self.mvn.update_mean_cov(v, iv)

        M, S = self.mvn.get_params()

        if N is not None:
            D = multivariate_normal.rvs(M, S, N)
            M = D.mean(axis=0)
            S = np.cov(D.T)

        return M, S

    def get_memmap(self, X):
        import os
        from joblib import dump, load

        folder = './joblib_memmap'
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass

        data_filename_memmap = os.path.join(folder, 'data_memmap')
        dump(X, data_filename_memmap)
        data = load(data_filename_memmap, mmap_mode='r')
        return data

    def predict_proba(self, X, n_jobs=-1, batch_size=5000, parallel=True):
        """
        Predict probability.

        :param X: data.
        :param n_jobs: Number of jobs.
        :param batch_size: Batch size.
        :param parallel: Parallel computation?
        :return: Probabilities.
        """
        num_data = X.shape[0]
        num_nodes = self.dag.number_of_nodes()
        D = self.get_memmap(X)

        all_units = []
        for row_id in range(num_data):
            units = []
            for node_id in range(num_nodes):
                if self.__has_parents__(node_id) is False:
                    m = self.params.means[node_id]
                    s = math.sqrt(self.params.cov[node_id, node_id])
                    unit = WORK_UNIT(row_id, node_id, m, s, None)
                    units.append(unit)
                else:
                    m = self.params.means
                    s = self.params.cov
                    dep = sorted(self.dag.parents(node_id))
                    unit = WORK_UNIT(row_id, node_id, m, s, dep)
                    units.append(unit)
            all_units.append(WORK_UNITS(row_id, units))

        jobs = n_jobs if parallel is True else 1
        results = Parallel(n_jobs=jobs,
                           backend='threading',
                           batch_size=batch_size)(delayed(__get_probs__)(D, W) for W in all_units)
        results = sorted(results, key=lambda r: r.row_id)
        results = list(map(lambda r: r.prob, results))

        return np.array(results)

    def predict_log_proba(self, X, n_jobs=-1, batch_size=5000, parallel=True):
        """
        Predict log probabilities.

        :param X: Data.
        :param n_jobs: Number of jobs.
        :param batch_size: Batch size.
        :param parallel: Compute in parallel?
        :return: Log probabilities.
        """
        num_data = X.shape[0]
        num_nodes = self.dag.number_of_nodes()
        D = self.get_memmap(X)

        all_units = []
        for row_id in range(num_data):
            units = []
            for node_id in range(num_nodes):
                if self.__has_parents__(node_id) is False:
                    m = self.params.means[node_id]
                    s = math.sqrt(self.params.cov[node_id, node_id])
                    unit = WORK_UNIT(row_id, node_id, m, s, None)
                    units.append(unit)
                else:
                    m = self.params.means
                    s = self.params.cov
                    dep = sorted(self.dag.parents(node_id))
                    unit = WORK_UNIT(row_id, node_id, m, s, dep)
                    units.append(unit)
            all_units.append(WORK_UNITS(row_id, units))

        jobs = n_jobs if parallel is True else 1
        results = Parallel(n_jobs=jobs,
                           backend='threading',
                           batch_size=batch_size)(delayed(__get_log_probs__)(D, W) for W in all_units)
        results = sorted(results, key=lambda r: r.row_id)
        results = list(map(lambda r: r.prob, results))

        return np.array(results)

    def log_prob(self, X):
        """
        Computes the log probabilities.

        :param X: Data.
        :return: Log probabilities.
        """
        num_nodes = self.dag.number_of_nodes()
        sum = 0.0
        for node_id in range(num_nodes):
            if self.__has_parents__(node_id) is False:
                d = X[:, node_id]
                m = self.params.means[node_id]
                s = np.sqrt(self.params.cov[node_id, node_id])
                logp = np.sum([np.log10(p) for p in dnorm(d, m, s)])
                sum += logp
            else:
                m = self.params.means
                s = self.params.cov
                dep = sorted(self.dag.parents(node_id))
                logp = np.sum([np.log10(p) for p in dcmvnorm(X, m, s, node_id, dep)])
                sum += logp
        return sum
