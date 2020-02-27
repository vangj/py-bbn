import json

import networkx as nx

from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.graph import Graph
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable


class Dag(Graph):
    """
    Directed acyclic graph.
    """

    def __init__(self):
        """
        Ctor.
        """
        Graph.__init__(self)

    def get_parents(self, id):
        """
        Gets the parent IDs of the specified node.

        :param id: Node id.
        :return: Array of parent ids.
        """
        return [x for x in self.edge_map if id in self.edge_map[x]]

    def get_children(self, node_id):
        """
        Gets the children IDs of the specified node.

        :param node_id: Node id.
        :return: Array of children ids.
        """
        return [x for x in self.edge_map[node_id]]

    def __shouldadd__(self, edge):
        """
        Checks if the specified directed edge should be added.

        :param edge: Directed edge.
        :return: A boolean indicating if the edge should be added.
        """
        if EdgeType.DIRECTED != edge.type:
            return False

        parent = edge.i
        child = edge.j

        if parent.id == child.id:
            return False

        if child.id not in self.edge_map[parent.id] and parent.id not in self.edge_map[child.id]:
            if not PathDetector(self, child.id, parent.id).exists():
                return True

        return False

    def edge_exists(self, id1, id2):
        """
        Checks if a directed edge exists between the specified id. e.g. id1 -> id2

        :param id1: Node id.
        :param id2: Node id.
        :return: A boolean indicating if a directed edge id1 -> id2 exists.
        """
        if id2 in self.edge_map[id1] and id1 not in self.edge_map[id2]:
            return True
        return False

    def to_nx_graph(self):
        """
        Converts this DAG to a NX DiGraph for visualization.

        :return: A tuple, where the first item is the NX DiGraph and the second items are the node labels.
        """
        g = nx.DiGraph()
        labels = []

        for k, node in self.nodes.items():
            g.add_node(node.id)
            t = (node.id, node.variable.name)
            labels.append(t)

        for k, edge in self.edges.items():
            pa = edge.i.id
            ch = edge.j.id
            g.add_edges_from([(pa, ch, {})])

        return g, dict(labels)


class Bbn(Dag):
    """
    BBN.
    """

    def __init__(self):
        """
        Ctor.
        """
        Dag.__init__(self)
        self.parents = {}

    def get_parents_ordered(self, id):
        """
        Gets the IDs of the specified node ordered.

        :param id: ID of node.
        :return: List of parent IDs sorted.
        """
        return sorted(self.parents[id]) if id in self.parents else []

    def __edge_added__(self, edge):
        if edge.j.id not in self.parents:
            self.parents[edge.j.id] = []

        if edge.i.id not in self.parents[edge.j.id]:
            self.parents[edge.j.id].append(edge.i.id)

    def __shouldadd__(self, edge):
        """
        Checks if the specified directed edge should be added.

        :param edge: Directed edge.
        :return: A boolean indicating if the directed edge should be added.
        """
        if isinstance(edge.i, BbnNode) and isinstance(edge.j, BbnNode):
            return True
        return Dag.__shouldadd__(edge)

    @staticmethod
    def to_csv(bbn, path):
        """
        Converts the specified BBN to CSV format.

        :param bbn: BBN.
        :param path: Path to file.
        :return: None.
        """
        with open(path, 'w') as f:
            for node in bbn.get_nodes():
                v = node.variable
                vals = ','.join(v.values)
                probs = ','.join([str(p) for p in node.probs])
                s_node = f'{v.id},{v.name},{vals},|,{probs}'
                f.write(s_node)
                f.write('\n')

            for _, edge in bbn.edges.items():
                t = 'directed' if edge.type == EdgeType.DIRECTED else 'undirected'
                s_edge = f'{edge.i.id},{edge.j.id},{t}'
                f.write(s_edge)
                f.write('\n')

    @staticmethod
    def from_csv(path):
        """
        Converts the BBN in CSV format to a BBN.
        :param path: Path to CSV file.
        :return: BBN.
        """
        with open(path, 'r') as f:
            nodes = {}
            edges = []

            for line in f:
                tokens = line.split(',')
                if 3 == len(tokens):
                    edge = int(tokens[0]), int(tokens[1])
                    edges.append(edge)
                else:
                    tokens = line.split('|')
                    v_part = [item.strip() for item in tokens[0].split(',') if len(item.strip()) > 0]
                    p_part = [item.strip() for item in tokens[1].split(',') if len(item.strip()) > 0]

                    i = int(v_part[0])
                    v = Variable(i, v_part[1], v_part[2:])
                    p = [float(p) for p in p_part]

                    node = BbnNode(v, p)
                    nodes[i] = node

            bbn = Bbn()
            for _, node in nodes.items():
                bbn.add_node(node)
            for edge in edges:
                pa_id, ch_id = edge

                pa = nodes[pa_id]
                ch = nodes[ch_id]

                bbn.add_edge(Edge(pa, ch, EdgeType.DIRECTED))
            return bbn

    @staticmethod
    def to_dict(bbn):
        """
        Gets a JSON serializable dictionary representation.

        :param bbn: BBN.
        :return: Dictionary.
        """
        return {
            'nodes': {n.id: n.to_dict() for n in bbn.get_nodes()},
            'edges': [{'pa': edge.i.id, 'ch': edge.j.id} for _, edge in bbn.edges.items()]
        }

    @staticmethod
    def from_dict(d):
        """
        Creates a BBN from a dictionary (deserialized JSON).

        :param d: Dictionary.
        :return: BBN.
        """

        def get_variable(d):
            return Variable(d['id'], d['name'], d['values'])

        def get_bbn_node(d):
            return BbnNode(get_variable(d['variable']), d['probs'])

        nodes = {k: get_bbn_node(n) for k, n in d['nodes'].items()}
        edges = d['edges']

        bbn = Bbn()

        for k, n in nodes.items():
            bbn.add_node(n)

        for e in edges:
            pa_id = e['pa']
            ch_id = e['ch']

            pa = nodes[pa_id] if pa_id in nodes else nodes[str(pa_id)]
            ch = nodes[ch_id] if ch_id in nodes else nodes[str(ch_id)]

            bbn.add_edge(Edge(pa, ch, EdgeType.DIRECTED))

        return bbn

    @staticmethod
    def to_json(bbn, path):
        """
        Serializes BBN to JSON.

        :param bbn: BBN.
        :param path: Path.
        :return: None.
        """
        s = json.dumps(Bbn.to_dict(bbn), indent=2)
        with open(path, 'w') as f:
            f.write(s)

    @staticmethod
    def from_json(path):
        """
        Deserializes BBN from JSON.

        :param path: Path.
        :return: BBN.
        """
        with open(path, 'r') as f:
            d = json.loads(f.read())
            bbn = Bbn.from_dict(d)
            return bbn


class PathDetector(object):
    """
    Detects path between two nodes.
    """

    def __init__(self, graph, start, stop):
        """
        Ctor.

        :param graph: DAG.
        :param start: Start node id.
        :param stop: Stop node id.
        """
        self.graph = graph
        self.start = start
        self.stop = stop
        self.seen = set()

    def exists(self):
        """
        Checks if a path exists.

        :return: True if a path exists, otherwise, false.
        """
        if self.start == self.stop:
            return True
        else:
            return self.__find__(self.start)

    def __find__(self, i):
        """
        Checks if a path exists from the specified node to the stop node.

        :param i: Node id.
        :return: True if a path exists, otherwise, false.
        """
        children = self.graph.get_children(i)
        if self.stop in children:
            return True

        self.seen.add(i)
        for child in children:
            if child not in self.seen and self.__find__(child):
                return True

        return False


class BbnUtil(object):
    """
    BBN utility.
    """

    @staticmethod
    def get_huang_graph():
        """
        Gets the Huang reference BBN graph.

        :return: BBN.
        """
        a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
        b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
        c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])
        d = BbnNode(Variable(3, 'd', ['on', 'off']), [0.9, 0.1, 0.5, 0.5])
        e = BbnNode(Variable(4, 'e', ['on', 'off']), [0.3, 0.7, 0.6, 0.4])
        f = BbnNode(Variable(5, 'f', ['on', 'off']), [0.01, 0.99, 0.01, 0.99, 0.01, 0.99, 0.99, 0.01])
        g = BbnNode(Variable(6, 'g', ['on', 'off']), [0.8, 0.2, 0.1, 0.9])
        h = BbnNode(Variable(7, 'h', ['on', 'off']), [0.05, 0.95, 0.95, 0.05, 0.95, 0.05, 0.95, 0.05])

        bbn = Bbn() \
            .add_node(a) \
            .add_node(b) \
            .add_node(c) \
            .add_node(d) \
            .add_node(e) \
            .add_node(f) \
            .add_node(g) \
            .add_node(h) \
            .add_edge(Edge(a, b, EdgeType.DIRECTED)) \
            .add_edge(Edge(a, c, EdgeType.DIRECTED)) \
            .add_edge(Edge(b, d, EdgeType.DIRECTED)) \
            .add_edge(Edge(c, e, EdgeType.DIRECTED)) \
            .add_edge(Edge(d, f, EdgeType.DIRECTED)) \
            .add_edge(Edge(e, f, EdgeType.DIRECTED)) \
            .add_edge(Edge(c, g, EdgeType.DIRECTED)) \
            .add_edge(Edge(e, h, EdgeType.DIRECTED)) \
            .add_edge(Edge(g, h, EdgeType.DIRECTED))

        return bbn

    @staticmethod
    def get_simple():
        """
        Gets a simple BBN graph.

        :return: BBN.
        """
        a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
        b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
        c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])
        d = BbnNode(Variable(3, 'd', ['on', 'off']), [0.9, 0.1, 0.5, 0.5])
        e = BbnNode(Variable(4, 'e', ['on', 'off']), [0.3, 0.7, 0.6, 0.4])
        f = BbnNode(Variable(5, 'f', ['on', 'off']), [0.01, 0.99, 0.01, 0.99, 0.01, 0.99, 0.99, 0.01])

        bbn = Bbn() \
            .add_node(a) \
            .add_node(b) \
            .add_node(c) \
            .add_node(d) \
            .add_node(e) \
            .add_node(f) \
            .add_edge(Edge(a, b, EdgeType.DIRECTED)) \
            .add_edge(Edge(a, c, EdgeType.DIRECTED)) \
            .add_edge(Edge(b, d, EdgeType.DIRECTED)) \
            .add_edge(Edge(c, e, EdgeType.DIRECTED)) \
            .add_edge(Edge(d, f, EdgeType.DIRECTED)) \
            .add_edge(Edge(e, f, EdgeType.DIRECTED))

        return bbn
