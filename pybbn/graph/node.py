from pybbn.graph.util import IdUtil

class Node:
    def __init__(self, id):
        self.id = id
        self.metadata = dict()

    def add_metadata(self, k, v):
        self.metadata[k] = v


class BbnNode(Node):
    def __init__(self, variable, probs):
        Node.__init__(self, variable.id)
        self.variable = variable
        self.probs = probs

    def get_weight(self):
        return len(self.variable.values)


class Clique(Node):
    def __init__(self, nodes):
        nids = [n.id for n in nodes]
        nids.sort()
        sid = str.join('-', [str(x) for x in nids])
        id = IdUtil.hash_string(sid)
        Node.__init__(self, id)
        self.nodes = nodes
        self.marked = False

    def is_marked(self):
        return self.marked

    def mark(self):
        self.marked = True

    def unmark(self):
        self.marked = False

    def is_superset(self, that):
        s1 = [node.id for node in self.nodes]
        s2 = [node.id for node in that.nodes]
        s3 = [id for id in s1 if id in s2]

        if len(s2) == len(s3):
            return True
        else:
            return False

    def get_weight(self):
        weight = 1
        for node in self.nodes:
            weight = weight * node.get_weight()
        return weight

    def contains(self, id):
        result = len([n for n in self.nodes if n.id == id])
        if result > 0:
            return True
        else:
            return False

    def get_sep_set(self, that):
        return SepSet(self, that)


class SepSet(Clique):
    def __init__(self, left, right):
        lhs = [x.id for x in left.nodes]
        rhs = [x.id for x in right.nodes]
        intersection = [x for x in lhs if x in rhs]
        nodes = [x for x in left.nodes if x.id in intersection]
        Clique.__init__(self, nodes)
        self.left = left
        self.right = right

    def get_cost(self):
        return self.left.get_weight() + self.right.get_weight()

    def get_mass(self):
        return len(self.nodes)

