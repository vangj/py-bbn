import itertools
import json

from libpgm.discretebayesiannetwork import DiscreteBayesianNetwork
from libpgm.graphskeleton import GraphSkeleton
from libpgm.nodedata import NodeData

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
        Look <a href="https://pythonhosted.org/libpgm/unittestdict.html">here</a>.
        :param j: String representing JSON.
        :return: py-bbn BBN.
        """
        return Factory.from_libpgm_discrete_dictionary(json.loads(j))

    @staticmethod
    def from_libpgm_discrete_dictionary(d):
        """
        Converts a libpgm discrete network as specified by a dictionary into a py-bbn one.
        Look <a href="https://pythonhosted.org/libpgm/unittestdict.html">here</a>.
        :param d: A dictionary representing a libpgm discrete network.
        :return: py-bbn BBN.
        """
        nd = NodeData()
        nd.Vdata = d['Vdata']

        skel = GraphSkeleton()
        skel.V = d['V']
        skel.E = d['E']
        skel.toporder()

        bn = DiscreteBayesianNetwork(skel, nd)
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
                parents = bn.Vdata[name]['parents']
                domains = []

                if parents is None or len(parents) == 0:
                    return domains

                for parent in parents:
                    domain = bn.Vdata[parent]['vals'][:]
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
                joiner_delim = ', ' if domain_spaces is True else ','
                s = []
                for pa_domain in pa_domains:
                    r = joiner_delim.join(["'{}'".format(v) for v in pa_domain])
                    r = '[{}]'.format(r)
                    s.append(r)
                return s

            def get_cond_probs(name, bn, domain_spaces=True):
                probs = []
                pa_domains = stringify_cross_product(cross_product(get_parent_domains(name, bn)), domain_spaces)
                if len(pa_domains) == 0:
                    probs = bn.Vdata[name]['cprob'][:]
                else:
                    for pa_domain in pa_domains:
                        cprob = bn.Vdata[name]['cprob'][pa_domain]
                        for p in cprob:
                            probs.append(p)

                return probs

            nodes = {}
            idx = 0
            for name in bn.V:
                domain = bn.Vdata[name]['vals'][:]
                probs = get_cond_probs(name, bn, domain_spaces)
                node = BbnNode(Variable(idx, name, domain), probs)
                nodes[name] = node
                idx += 1
            return nodes

        def get_edges(bn, nodes):
            edges = []
            for e in bn.E:
                pa = nodes[e[0]]
                ch = nodes[e[1]]
                edge = Edge(pa, ch, EdgeType.DIRECTED)
                edges.append(edge)
            return edges

        nodes = get_nodes(bn)
        edges = get_edges(bn, nodes)

        bbn = Bbn()

        for k, v in nodes.iteritems():
            bbn.add_node(v)

        for e in edges:
            bbn.add_edge(e)

        return bbn
