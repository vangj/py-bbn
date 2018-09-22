import itertools

import networkx as nx
import numpy as np
from networkx.algorithms.dag import is_directed_acyclic_graph

from pybbn.graph.dag import Bbn
from pybbn.graph.edge import EdgeType, Edge
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable


class MwstAlgo(object):
    """
    Maximum weight spanning tree algorithm. Also known as Chow-Liu algorithm.
    """
    def __init__(self):
        """
        Ctor.
        """
        self.data = None
        self.bbn = None

    def fit(self, data):
        """
        Learns the structure and parameter of a Bayesian belief network from the data.
        :param data: Data.
        :return: BBN.
        """
        g = self.learn_structure(data)
        p = self.learn_parameters(data, g)

        bbn = build_bbn(data.variable_profiles, g, p)

        self.data = data
        self.bbn = bbn

    def learn_parameters(self, data, g):
        """
        Learns the parameters (conditional probability tables, local probability models).
        :param data: Data.
        :param g: DAG.
        :return: A dictionary associated with nodes/variables and their parameters.
        """
        cpts = {}
        variable_profiles = data.variable_profiles
        nodes = list(g.nodes)
        for idx in nodes:
            child = g.nodes[idx]['name']
            c_values = variable_profiles[child]

            parents = list(g.predecessors(idx))
            parents = [g.nodes[pa_id]['name'] for pa_id in parents]
            p_values = list(itertools.product(*[variable_profiles[name] for name in parents]))

            if len(parents) == 0:
                cpt = [data.__get_prob__(child, value) for value in c_values]
            else:
                cpt = []
                for values in p_values:
                    for value in c_values:
                        p = data.__get_cond_prob_set__(child, value, parents, values)
                        cpt.append(p)
            cpts[idx] = cpt

        return cpts

    def learn_structure(self, data):
        """
        Learns the BBN structure.
        :param data: Data.
        :return: DAG.
        """
        # gets the skeleton, which is a tree, undirected graph
        u = get_mwst_skeleton(data)

        # gets all the v-structures, if any
        variables = data.get_variables(by_name=False)
        v_structures = []
        for v_structure in get_v_structures(u):
            name1 = variables[v_structure[0]]
            name2 = variables[v_structure[2]]
            names = [variables[v_structure[1]]]
            cmi, result = data.is_cond_dep(name1, name2, names)
            if result is True:
                t = (v_structure[0], v_structure[1], v_structure[2], cmi)
                v_structures.append(t)
        v_structures = sorted(v_structures, key=lambda t: t[3], reverse=True)

        # create the DAG, this graph will have edges oriented
        g = nx.DiGraph()
        for idx in u.nodes:
            g.add_node(idx, name=u.nodes[idx]['name'])

        # attempt to orient edges by v-structures
        for v_structure in v_structures:
            left_node = v_structure[0]
            mid_node = v_structure[1]
            right_node = v_structure[2]

            edge1 = (left_node, mid_node, {})
            edge2 = (right_node, mid_node, {})

            g.add_edges_from([edge1, edge2])

            if is_directed_acyclic_graph(g) is False:
                g.remove_edges_from([edge1, edge2])

        # attempt to orient by likelihood
        # FIXME: note this can create v-structures
        missing_edges = get_missing_edges(u, g)
        directed_edges = get_likely_directed_edges(missing_edges, data)
        for edge in directed_edges:
            pa_node = edge[0]
            ch_node = edge[1]
            dedge = (pa_node, ch_node, {})
            g.add_edges_from([dedge])

            if is_directed_acyclic_graph(g) is False:
                g.remove_edges_from([dedge])

        # now just orient randomly, so long as the graph is a dag
        missing_edges = get_missing_edges(u, g)
        while len(missing_edges) != 0:
            for edge in missing_edges:
                pa_id = np.random.randint(0, 2)
                ch_id = 1 if pa_id == 0 else 0

                pa_node = edge[pa_id]
                ch_node = edge[ch_id]

                dedge = (pa_node, ch_node, {})
                g.add_edges_from([dedge])

                if is_directed_acyclic_graph(g) is False:
                    g.remove_edges_from([dedge])

            missing_edges = get_missing_edges(u, g)

        return g


def build_bbn(variable_profiles, g, p):
    """
    Builds a BBN from a DAG, g, and paremeters, p.
    :param variable_profiles: Variable profiles.
    :param g: DAG.
    :param p: Parameters.
    :return: BBN.
    """
    bbn = Bbn()
    nodes = list(g.nodes)
    bbn_node_dict = {}
    for idx in nodes:
        name = g.nodes[idx]['name']
        domain = variable_profiles[name]
        cpt = p[idx]

        v = Variable(idx, name, domain)
        n = BbnNode(v, cpt)
        bbn.add_node(n)
        bbn_node_dict[idx] = n

    edges = list(g.edges)
    for edge in edges:
        pa = bbn_node_dict[edge[0]]
        ch = bbn_node_dict[edge[1]]
        e = Edge(pa, ch, EdgeType.DIRECTED)
        bbn.add_edge(e)

    return bbn


def get_likely_directed_edges(edges, data):
    """
    Gets directed edged based on likelihood for each undirected edge.
    :param edges: List of edges.
    :param data: Data.
    :return: List of directed edge.
    """
    directed_edges = []
    variables = data.get_variables(by_name=False)
    for edge in edges:
        v1 = variables[edge[0]]
        v2 = variables[edge[1]]

        v1_v2 = data.get_local_kutato(v1, [v2])
        v2_v1 = data.get_local_kutato(v2, [v1])
        if v1_v2 > v2_v1:
            t = (edge[0], edge[1])
            directed_edges.append(t)
        elif v1_v2 < v2_v1:
            t = (edge[1], edge[0])
            directed_edges.append(t)
    return directed_edges


def get_missing_edges(u, g):
    """
    Gets the missing edges in g that is in u.
    :param u: Undirected graph.
    :param g: Directed acyclic graph.
    :return: List of tuples, where each tuple is a pair of nodes designating an edge.
    """
    edges = []
    for edge in list(u.edges):
        n1 = edge[0]
        n2 = edge[1]

        if n1 not in list(g.adj[n2]) and n2 not in list(g.adj[n1]):
            t = (n1, n2)
            edges.append(t)
    return edges


def get_v_structures(g):
    """
    Gets all the v-structures in g. For three nodes, a, b, c, where a is connected to b,
    b is connected c, and a and c are not connected, this configuration is called a v-structure.
    :param g: Undirected graph.
    :return: List of tuples representing v-structure.
    """
    v_structures = []

    nodes = list(g.nodes)
    for node in nodes:
        neighbors = list(g.adj[node])
        for ne1 in neighbors:
            for ne2 in neighbors:
                if ne1 < ne2 and ne1 not in g.adj[ne2] and ne2 not in g.adj[ne1]:
                    t = (ne1, node, ne2)
                    v_structures.append(t)

    return v_structures


def get_mwst_skeleton(data):
    """
    Gets the undirected graph that represents the maximum weight spanning tree (MWST)
    of the data.
    :param data: Data.
    :return: Undirected graph (MWST).
    """
    g = nx.Graph()
    variables = data.get_variables()
    for k, v in variables.items():
        g.add_node(v, name=k)

    mis = data.get_pairwise_mutual_information()
    for mi in mis:
        lhs_node = variables[mi[0]]
        rhs_node = variables[mi[1]]
        t = (lhs_node, rhs_node, {})
        g.add_edges_from([t])

        if len(g.edges) == len(variables) - 1:
            break

    return g
