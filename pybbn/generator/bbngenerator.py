import json

import networkx as nx
import numpy as np
from networkx.algorithms.dag import is_directed_acyclic_graph
from networkx.algorithms.shortest_paths.generic import shortest_path
from scipy.stats import dirichlet

from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable


def __get_simple_ordered_tree__(n):
    """
    Generates a simple-ordered tree. The tree is just a
    directed acyclic graph of n nodes with the structure
    0 --> 1 --> .... --> n.
    :param n: Number of nodes.
    :return: A directed graph.
    """
    g = nx.DiGraph()

    for i in range(n):
        g.add_node(i)

    for i in range(n - 1):
        g.add_edges_from([(i, i + 1, {})])
    return g


def __convert_to_undirected_graph__(g):
    """
    Converts a directed acyclic graph (DAG) to an undirected graph.
    We need to convert a DAG to an undirected one to use
    some API calls to operate over the undirected graph. For example,
    in checking for connectedness of a graph, the API has a method
    to check for connectedness of an undirected graph, but not a
    DAG.
    :param g: Graph.
    :return: An undirected graph.
    """
    u = nx.Graph()
    for n in g.nodes:
        u.add_node(n)
    for e in g.edges:
        u.add_edges_from([(e[0], e[1], {})])
    return u


def __is_connected__(g):
    """
    Checks if a the directed acyclic graph is connected.
    :return: A boolean indicating if the graph is connected.
    """
    u = __convert_to_undirected_graph__(g)
    return nx.is_connected(u)


def __get_random_node_pair__(n):
    """
    Randomly generates a pair of nodes.
    :param n: Number of nodes.
    :return: A tuple of random nodes.
    """
    i = np.random.randint(0, n)
    j = i
    while j == i:
        j = np.random.randint(0, n)
    return i, j


def __edge_exists__(i, j, g):
    """
    Checks if the edge i --> j exists in the graph, g.
    :param i: Index of a node.
    :param j: Index of a node.
    :param g: Graph.
    :return: A boolean indicating if j is a successor of i.
    """
    return j in list(g.successors(i))


def __del_edge__(i, j, g):
    """
    Deletes the edge i --> j in the graph, g. The edge is only
    deleted if this removal does NOT cause the graph to be
    disconnected.
    :param i: Index of a node.
    :param j: Index of a node.
    :param g: Graph.
    :return: None
    """
    if g.has_edge(i, j) is True:
        g.remove_edge(i, j)

        if __is_connected__(g) is False:
            g.add_edges_from([(i, j, {})])


def __add_edge__(i, j, g):
    """
    Adds an edge i --> j to the graph, g. The edge is only
    added if this addition does NOT cause the graph to have
    cycles.
    :param i: Index of a node.
    :param j: Index of a node.
    :param g: Graph.
    :return: None
    """
    g.add_edges_from([(i, j, {})])
    if is_directed_acyclic_graph(g) is False:
        g.remove_edge(i, j)


def __find_predecessor__(i, j, g):
    """
    Finds a predecessor, k, in the path between two nodes, i and j,
    in the graph, g. We assume g is connected, and there is a
    path between i and j (ignoring the direction of the edges).
    We want to find a k, that is a parent of j, that is in
    the path between i and j. In some cases, we may not find
    such a k.
    :param i: Index of node.
    :param j: Index of node.
    :param g: Graph.
    :return: Returns predecessor, if any, or None.
    """
    parents = list(g.predecessors(j))
    u = __convert_to_undirected_graph__(g)
    for pa in parents:
        try:
            shortest_path(u, pa, i)
            return pa
        except nx.NetworkXNoPath:
            pass
    return None


def __generate_multi_connected_structure__(n, max_iter=10):
    """
    Generates a multi-connected directed acyclic graph.
    :param n: Number of nodes.
    :param max_iter: Maximum iterations.
    :return: Graph structure (networkx).
    """
    g = __get_simple_ordered_tree__(n)
    for it in range(max_iter):
        i, j = __get_random_node_pair__(n)
        if g.has_edge(i, j) is True:
            __del_edge__(i, j, g)
        else:
            __add_edge__(i, j, g)
    return g


def __generate_singly_structure__(n, max_iter=10):
    """
    Generates a singly-connected directed acyclic graph.
    :param n: Number of nodes.
    :param max_iter: Maximum iterations.
    :return: Graph structure (networkx).
    """
    g = __get_simple_ordered_tree__(n)

    for it in range(max_iter):
        i, j = __get_random_node_pair__(n)
        if g.has_edge(i, j) is True or g.has_edge(j, i) is True:
            pass
        else:
            p = np.random.random()
            k = __find_predecessor__(i, j, g)
            if k is not None:
                g.remove_edge(k, j)
                if p < 0.5:
                    g.add_edges_from([(j, i, {})])
                else:
                    g.add_edges_from([(i, j, {})])

                if __is_connected__(g) is False:
                    g.add_edges_from([(k, j, {})])

                    if p < 0.5:
                        g.remove_edge(j, i)
                    else:
                        g.remove_edge(i, j)
    return g


def __generate_num_values__(n, max_values=2):
    """
    For each node, i, in the nodes, n, determine the number of values
    the node (or equivalently, variable) has. Every node/variable in a
    Bayesian Network should have 2 or more values. This generates
    the number of values each variable will have. Each number will be
    sampled uniformly.
    :param n: Number of nodes.
    :param max_values: Maximum number of values for a node.
    :return: Array of number of values for each node.
    """
    return np.array([max(np.random.randint(0, max_values) + 1, 2) for _ in range(n)])


def __generate_alphas__(n, max_alpha=10):
    """
    Generate random number for the alpha's (the hyperparameters).
    Each number will be in the range [1, max_alpha]. Each number will
    be sampled uniformly.
    :param n: Number of alpha's to sample.
    :param max_alpha: Maximum alpha value.
    :return: A list of alpha's.
    """
    return [np.random.randint(1, max_alpha + 1) for i in range(n)]


def __sample_dirichlet__(n, max_alpha=10):
    """
    Samples from the Dirichlet distribution to a produce
    a probability vector of length n. The sum of each probability
    in the probability vector should sum to 1.
    :param n: Number of alpha's to sample.
    :param max_alpha: The maximum alpha.
    :return: Array of Dirichlet distributed values.
    """
    return np.array(dirichlet.rvs(__generate_alphas__(n, max_alpha))[0])


def __get_num_parent_instantiations__(parents, num_values):
    """
    Gets the number of parent instantiations.
    :param parents: List of parent indices.
    :param num_values: List of the number of values per node.
    :return: Number of parent instantiations.
    """
    num_pa_instantiations = 1
    for pa in parents:
        num_pa_values = num_values[pa]
        num_pa_instantiations *= num_pa_values
    return num_pa_instantiations


def __generate_dirichlet_parameters__(i, parents, num_values, max_alpha=10):
    """
    Randomly and uniformly generate parameters for a node i. A matrix
    of parameters will be returned. The matrix will represent the
    condtional probability table of the node i. The matrix will have
    the dimensions m (rows) by n (columns), m x n, where m is the
    product of the domain sizes of the parents, and n is the domain
    size of the node. The domain size is just the number of values
    that a node (variable) has, which should always be greater than
    or equal to 2.
    :param i: The index of the node for which parameters are being generated.
    :param parents: The indices of the parents of the node.
    :param num_values: The number of values desired.
    :param max_alpha: The maximum alpha per value.
    :return: A conditional probability table (CPT) that specifies the local probability model for the node.
    """
    num_pa_instantiations = __get_num_parent_instantiations__(parents, num_values)

    n = num_values[i]
    cpt = []
    for pa_instantiation in range(num_pa_instantiations):
        probs = __sample_dirichlet__(n, max_alpha)
        cpt.append(probs)
    return np.array(cpt)


def __generate_parameters__(g, max_values=2, max_alpha=10):
    """
    Generates parameters for each node in the graph, g.
    A dictionary indexed by the node's id will give its
    (sampled) parameters and its parents.
    :param max_values: Maximum values per node.
    :param max_alpha: Maximum alpha per value (hyperparameters).
    :return: Parameters.
    """
    num_nodes = len(list(g.nodes))
    num_values = __generate_num_values__(num_nodes, max_values)
    g_params = {}
    for i in g.nodes:
        parents = list(g.predecessors(i))
        params = __generate_dirichlet_parameters__(i, parents, num_values, max_alpha)
        g_params[i] = {
            'parents': parents,
            'params': params,
            'shape': [__get_num_parent_instantiations__(parents, num_values), num_values[i]]
        }
    return g_params


def to_json(g, params, pretty=False):
    """
    Serializes the graph to JSON.
    :param g: Graph.
    :param params: Parameters.
    :param pretty: Pretty-print serialization flag.
    :return: None.
    """
    j = {
        'nodes': list(g.nodes),
        'edges': [{'pa': e[0], 'ch': e[1]} for e in g.edges],
        'parameters': [{
                'node': k,
                'params': list(v['params'].flatten()),
                'shape': v['shape']} for k, v in params.items()
        ]}

    return json.dumps(j, indent=2, sort_keys=False) if pretty is True else json.dumps(j)


def generate_multi_bbn(n, max_iter=10, max_values=2, max_alpha=10):
    """
    Generates structure and parameters for a multi-connected BBN.
    :param n: Number of nodes.
    :param max_iter: Maximum iterations.
    :param max_values: Maximum values per node.
    :param max_alpha: Maximum alpha per value (hyperparameters).
    :return: A tuple of structure and parameters.
    """
    g = __generate_multi_connected_structure__(n, max_iter)
    p = __generate_parameters__(g, max_values, max_alpha)
    return g, p


def generate_singly_bbn(n, max_iter=10, max_values=2, max_alpha=10):
    """
    Generates structure and parameters for a singly-connected BBN.
    :param n: Number of nodes.
    :param max_iter: Maximum iterations.
    :param max_values: Maximum values per node.
    :param max_alpha: Maximum alpha per value (hyperparameters).
    :return: A tuple of structure and parameters.
    """
    g = __generate_singly_structure__(n, max_iter)
    p = __generate_parameters__(g, max_values, max_alpha)
    return g, p


def convert_for_exact_inference(g, p):
    """
    Converts the graph and parameters to a BBN.
    :param g: Directed acyclic graph (DAG in the form of networkx).
    :param p: Parameters.
    :return: BBN.
    """
    bbn = Bbn()

    bbn_nodes = {}

    for node in g.nodes:
        id = node
        params = p[id]['params'].flatten()
        states = ['state{}'.format(state) for state in range(p[id]['shape'][1])]
        v = Variable(id, str(id), states)
        n = BbnNode(v, params)
        bbn.add_node(n)
        bbn_nodes[id] = n

    for e in g.edges:
        pa = bbn_nodes[e[0]]
        ch = bbn_nodes[e[1]]
        bbn.add_edge(Edge(pa, ch, EdgeType.DIRECTED))

    return bbn


def convert_for_drawing(bbn):
    """
    Converts a BBN to a networkx graph for drawing.
    :param bbn: BBN.
    :return: Directed acyclic graph.
    """
    g = nx.DiGraph()

    for k, v in bbn.nodes.iteritems():
        g.add_node(v.id)

    for k, e in bbn.edges.iteritems():
        pa = e.i.id
        ch = e.j.id
        g.add_edges_from([(pa, ch, {})])

    return g
