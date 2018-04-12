import math

import networkx as nx
import numpy as np
from networkx.algorithms.dag import topological_sort, is_directed_acyclic_graph

from pybbn.lg.gaussian import rnorm, dnorm, dcmvnorm, RandCondMvn


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

    def __init__(self, dag, params, max_samples=9000, max_iters=1, mb=False):
        """
        Ctor. Note that the dimensions of the DAG and parameters must match.
        :param dag: DAG.
        :param params: Parameters (means and covariance).
        :param max_samples: Max number of samples to use for approximate inference per iteration. Default is 9,000.
        :param max_iters: Max number of iterations. Default is 1.
        :param mb: A boolean indicating if we are only sampling locally based on Markov Blanket. Default is False.
        """
        self.dag = dag
        self.params = params
        self.evidence = np.array([None for _ in range(dag.number_of_nodes())], dtype=float)
        self.max_samples = max_samples
        self.max_iters = max_iters
        self.mb = mb

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
        self.evidence = np.array([None for _ in range(self.dag.number_of_nodes())], dtype=float)

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

    def do_inference(self):
        """
        Conducts Gibbs sampling.
        :return: The expected state of every variable.
        """

        def get_init_value(bbn, node_id):
            """
            Gets a random initial value for the specified node. If the specified node has evidence set, then that value
            is returned.
            :param bbn: BBN.
            :param node_id: Node id.
            :return: Initial value.
            """
            if bbn.__has_evidence__(node_id):
                return bbn.get_evidence(node_id)
            else:
                m = bbn.params.means[node_id]
                stdev = math.sqrt(bbn.params.cov[node_id, node_id])
                return list(rnorm(1, m, stdev))[0]

        def get_nodes_selector(node_id, num_nodes):
            """
            Gets a selector for all the nodes except the specified node.
            :param node_id: Node id.
            :param num_nodes: Number of nodes.
            :return: Sorted array of node ids.
            """
            return sorted([i for i in range(num_nodes) if i != node_id])

        def get_rcmvnorm_dist(node_id, means, cov):
            """
            Gets a conditional multivariate normal distribution.
            :param node_id: Node id.
            :param means: Means.
            :param cov: Covariance.
            :return: Random conditional multivariate normal distribution.
            """
            num_nodes = cov.shape[0]
            other_nodes = get_nodes_selector(node_id, num_nodes)
            dist = RandCondMvn(means, cov, node_id, other_nodes)
            return dist

        def get_mb_rcmvnorm_dist(dag, node_id, means, cov):
            other_nodes = dag.markov_blanket(node_id)
            dist = RandCondMvn(means, cov, node_id, other_nodes)
            return dist

        def get_rcmvnorm_dists(means, cov):
            """
            Gets a dictionary of rcmvnorm distributions keyed by node ID.
            :param means: Means.
            :param cov: Covariance.
            :return: Dictionary of rcmvnorm distributions.
            """
            dists = {}
            for node_id in range(cov.shape[0]):
                dist = get_rcmvnorm_dist(node_id, means, cov)
                dists[node_id] = dist
            return dists

        def get_mb_rcmvnorm_dists(dag, means, cov):
            """

            :param dag:
            :param means:
            :param cov:
            :return:
            """
            dists = {}
            for node_id in range(cov.shape[0]):
                dist = get_mb_rcmvnorm_dist(dag, node_id, means, cov)
                dists[node_id] = dist
            return dists

        def get_sample(dag, sample, max_samples, dists, mb=False):
            """
            Gets a sample.
            :param dag: Directed acyclic graph.
            :param sample: Initial sample.
            :param max_samples: Max samples.
            :return: Final sample.
            """
            num_nodes = dag.number_of_nodes()

            for i in range(max_samples):
                i_sample = np.copy(sample)

                for node_id in range(num_nodes):
                    if self.__has_evidence__(node_id) is True:
                        x = self.get_evidence(node_id)
                        i_sample[node_id] = x
                    else:
                        other_nodes = dag.markov_blanket(node_id) if mb is True else get_nodes_selector(node_id,
                                                                                                        num_nodes)
                        X = i_sample[other_nodes]
                        i_sample[node_id] = dists[node_id].next(X)

                sample = (sample + i_sample) / 2.0
            return sample

        num_nodes = self.dag.number_of_nodes()
        max_iters = self.max_iters
        outcome = np.zeros((1, num_nodes))
        dists = get_mb_rcmvnorm_dists(self.dag, self.params.means,
                                      self.params.cov) if self.mb is True else get_rcmvnorm_dists(self.params.means,
                                                                                                  self.params.cov)

        for i in range(max_iters):
            sample = np.array([get_init_value(self, node_id) for node_id in range(num_nodes)], dtype=float)
            sample = get_sample(self.dag, sample, self.max_samples, dists, mb=self.mb)
            outcome = outcome + sample

        outcome = outcome / float(max_iters)
        return outcome[0]

    def log_prob(self, data):
        num_nodes = self.dag.number_of_nodes()
        sum = 0.0
        for node_id in range(num_nodes):
            if self.__has_parents__(node_id) is False:
                d = data[:, node_id]
                m = self.params.means[node_id]
                s = math.sqrt(self.params.cov[node_id, node_id])
                logp = np.sum([math.log10(p) for p in dnorm(d, m, s)])
                sum += logp
            else:
                m = self.params.means
                s = self.params.cov
                dep = sorted(self.dag.parents(node_id))
                logp = np.sum([math.log10(p) for p in dcmvnorm(data, m, s, node_id, dep)])
                sum += logp
        return sum
