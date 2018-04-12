from pybbn.graph.graph import Graph


class Pdag(Graph):
    """
    Partially directed acyclic graph.
    """

    def __init__(self):
        """
        Ctor.
        """
        Graph.__init__(self)

    def get_parents(self, id):
        """
        Gets the parent of the specified node id.
        :param id: Node id.
        :return: Array of parent ids.
        """
        return [x for x in self.map if id in self.map[x]]

    def get_out_nodes(self, id):
        """
        Gets all the out nodes for the node with the specified id. Out nodes are all connected ndoes that are
        not parents (do not have a directed arc into the specified node).
        :param id: Node id.
        :return: Array of out node ids.
        """
        parents = self.get_parents(id)
        neighbors = self.get_neighbors(id)
        out_nodes = [neighbor_id for neighbor_id in neighbors if neighbor_id not in parents]
        return out_nodes

    def __shouldadd__(self, edge):
        """
        Checks if the specified edge should be added.
        :param edge: Edge (could be directed or undirected).
        :return: A boolean indicating if the edge should be added.
        """
        parent = edge.i
        child = edge.j

        if parent.id == child.id:
            return False

        if child.id not in self.map[parent.id] and parent.id not in self.map[child.id]:
            if not PathDetector(self, child.id, parent.id).exists():
                return True

        return False

    def edge_exists(self, id1, id2):
        """
        Checks if the specified edge id1 -- id2 exists.
        :param id1: Node id.
        :param id2: Node id.
        :return: A boolean indicating if the edge exists.
        """
        if id2 in self.map[id1] or id1 in self.map[id2]:
            return True
        return False

    def directed_edge_exists(self, id1, id2):
        """
        Checks if the specified edge id1 -> id2 exists.
        :param id1: Node id.
        :param id2: Node id.
        :return: A boolean indicating if the edge exists.
        """
        if id2 in self.map[id1] and id1 not in self.map[id2]:
            return True
        return False


class PathDetector(object):
    """
    Detects path between two nodes.
    """

    def __init__(self, graph, start, stop):
        """
        Ctor.
        :param graph: Pdag.
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
        out_nodes = self.graph.get_out_nodes(i)
        if self.stop in out_nodes:
            return True

        self.seen.add(i)
        for out_node in out_nodes:
            if out_node not in self.seen and self.__find__(out_node):
                return True

        return False
