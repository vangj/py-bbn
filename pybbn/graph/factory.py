import itertools
import json
from itertools import product

import networkx as nx
import pandas as pd
from networkx.algorithms.dag import topological_sort

from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable


class Factory(object):
    """
    Factory to convert other API BBNs into py-bbn.
    """

    @staticmethod
    def from_libpgm_discrete_json(j):
        """
        Converts a libpgm discrete network as specified by a JSON string into a py-bbn one.
        Look at https://pythonhosted.org/libpgm/unittestdict.html.

        :param j: String representing JSON.
        :return: py-bbn BBN.
        """
        return Factory.from_libpgm_discrete_dictionary(json.loads(j))

    @staticmethod
    def from_libpgm_discrete_dictionary(d):
        """
        Converts a libpgm discrete network as specified by a dictionary into a py-bbn one.
        Look at https://pythonhosted.org/libpgm/unittestdict.html.

        :param d: A dictionary representing a libpgm discrete network.
        :return: py-bbn BBN.
        """

        class LibpgmBBN(object):
            def __init__(self, V, E, Vdata):
                self.V = V
                self.E = E
                self.Vdata = Vdata

        bn = LibpgmBBN(d["V"], d["E"], d["Vdata"])
        return Factory.from_libpgm_discrete_object(bn)

    @staticmethod
    def from_libpgm_discrete_object(bn):
        """
        Converts a libpgm discrete network object into a py-bbn one.

        :param bn: libpgm discrete BBN.
        :return: py-bbn BBN.
        """

        def get_nodes(bn, domain_spaces=True):
            def get_parent_domains(name, bn):
                parents = bn.Vdata[name]["parents"]
                domains = []

                if parents is None or len(parents) == 0:
                    return domains

                for parent in parents:
                    domain = bn.Vdata[parent]["vals"][:]
                    domains.append(domain)
                return domains

            def cross_product(domains):
                products = []

                if domains is None or len(domains) == 0:
                    return products

                for e in itertools.product(*domains):
                    products.append(e)
                return products

            def stringify_cross_product(pa_domains, domain_spaces=True):
                joiner_delim = ", " if domain_spaces is True else ","
                s = []
                for pa_domain in pa_domains:
                    r = joiner_delim.join(["'{}'".format(v) for v in pa_domain])
                    r = "[{}]".format(r)
                    s.append(r)
                return s

            def get_cond_probs(name, bn, domain_spaces=True):
                probs = []
                pa_domains = stringify_cross_product(
                    cross_product(get_parent_domains(name, bn)), domain_spaces
                )
                if len(pa_domains) == 0:
                    probs = bn.Vdata[name]["cprob"][:]
                else:
                    for pa_domain in pa_domains:
                        cprob = bn.Vdata[name]["cprob"][pa_domain]
                        probs.extend(cprob)

                return probs

            nodes = {}
            for name in bn.V:
                domain = bn.Vdata[name]["vals"][:]
                order = bn.Vdata[name]["ord"]
                probs = get_cond_probs(name, bn, domain_spaces)
                node = BbnNode(Variable(order, name, domain), probs)
                nodes[name] = node
            return nodes

        def get_edges(bn, nodes):
            edges = []
            for k, v in bn.Vdata.items():
                ch = nodes[k]
                if v["parents"] is not None and len(v["parents"]) > 0:
                    parents = [nodes[pa] for pa in v["parents"]]
                    for pa in parents:
                        edge = Edge(pa, ch, EdgeType.DIRECTED)
                        edges.append(edge)
            return edges

        nodes = get_nodes(bn)
        edges = get_edges(bn, nodes)

        bbn = Bbn()

        for node in sorted(nodes.values(), key=lambda n: n.id):
            bbn.add_node(node)

        for e in edges:
            bbn.add_edge(e)

        return bbn

    @staticmethod
    def from_data(structure, df):
        """
        Creates a BBN.

        :param structure: A dictionary where keys are names of children and values are list of parent names.
        :param df: A dataframe.
        :return: BBN.
        """

        def get_profile(df):
            profile = {}
            for c in df.columns:
                values = sorted(list(df[c].value_counts().index))
                profile[c] = values
            return profile

        def get_n2i(parents):
            g = nx.DiGraph()
            for k in parents:
                g.add_node(k)
            for ch, pas in parents.items():
                for pa in pas:
                    g.add_edge(pa, ch)
            nodes = list(topological_sort(g))
            return {n: i for i, n in enumerate(nodes)}

        def get_cpt(name, parents, n2v, df):
            parents = sorted(parents)
            n2v = {k: sorted(v) for k, v in n2v.items()}

            n = df.shape[0]

            cpts = []
            if len(parents) == 0:
                for v in n2v[name]:
                    c = df[df[name] == v].shape[0]
                    p = c / n
                    cpts.append(p)
            else:
                domains = [(n, d) for n, d in n2v.items() if n in parents]
                domains = sorted(domains, key=lambda tup: tup[0])
                domain_names = [tup[0] for tup in domains]
                domain_values = [tup[1] for tup in domains]
                domains = list(product(*domain_values))

                for values in domains:
                    probs = []
                    denom_q = " and ".join(
                        [f'{n}=="{v}"' for n, v in zip(domain_names, values)]
                    )
                    for v in n2v[name]:
                        numer_q = f'{name}=="{v}" and {denom_q}'

                        numer = df.query(numer_q).shape[0] / n
                        denom = df.query(denom_q).shape[0] / n

                        if denom == 0:
                            prob = 1e-5
                        else:
                            prob = numer / denom
                        probs.append(prob)
                    probs = pd.Series(probs)
                    probs = probs / probs.sum()
                    probs = list(probs)
                    cpts.extend(probs)

            return cpts

        n2v = get_profile(df)
        n2i = get_n2i(df)
        n2c = {n: get_cpt(n, structure[n], n2v, df) for n in structure}

        bbn = Bbn()

        nodes = {}
        for name in n2v:
            idx = n2i[name]
            values = n2v[name]
            cpts = n2c[name]

            v = Variable(idx, name, values)
            node = BbnNode(v, cpts)
            nodes[name] = node
            bbn.add_node(node)

        for ch, parents in structure.items():
            ch_node = nodes[ch]
            for pa in parents:
                pa_node = nodes[pa]

                edge = Edge(pa_node, ch_node, EdgeType.DIRECTED)
                bbn.add_edge(edge)

        return bbn
