import networkx as nx


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
        u = get_mwst_skeleton(data)

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
        return u


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
