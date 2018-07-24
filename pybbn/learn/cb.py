import networkx as nx
from networkx.algorithms.dag import is_directed_acyclic_graph


class MwstAlgo(object):
    """
    Maximum weight spanning tree algorithm. Also known as Chow-Liu algorithm.
    """
    def __init__(self):
        """
        Ctor.
        """
        pass

    def fit(self, data):
        """
        Learns the structure and parameter of a Bayesian belief network from the data.
        :param data: Data.
        :return: BBN.
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
        missing_edges = get_missing_edges(u, g)


        return u


def get_directed_edges(edges, data):
    pass


def get_missing_edges(u, g):
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
    for idx, name in enumerate(variables.keys()):
        g.add_node(idx, name=name)

    mis = data.get_pairwise_mutual_information()
    for mi in mis:
        lhs_node = variables[mi[0]]
        rhs_node = variables[mi[1]]
        t = (lhs_node, rhs_node, {})
        g.add_edges_from([t])

        if len(g.edges) == len(variables) - 1:
            break

    return g
