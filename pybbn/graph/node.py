from pybbn.graph.util import IdUtil


class Node:
    def __init__(self, id):
        self.id = id
        self.metadata = dict()

    def add_metadata(self, k, v):
        self.metadata[k] = v

    def __str__(self):
        return '{}'.format(self.id)


class BbnNode(Node):
    def __init__(self, variable, probs):
        Node.__init__(self, variable.id)
        self.variable = variable
        self.probs = probs
        self.potential = None

    def get_weight(self):
        return len(self.variable.values)

    def __str__(self):
        return '{}|{}|{}'.format(self.id, self.variable.name, str.join(',', self.variable.values))


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

    def get_node_ids(self):
        return [node.id for node in self.nodes]

    def is_superset(self, that):
        s1 = set(self.get_node_ids())
        s2 = set(that.get_node_ids())
        return s1.issuperset(s2)

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

    def __str__(self):
        names = sorted([node.variable.name for node in self.nodes])
        return '({})'.format(str.join(',', names))


class SepSet(Clique):
    def __init__(self, left, right):
        lhs = [x.id for x in left.nodes]
        rhs = [x.id for x in right.nodes]
        intersection = [x for x in lhs if x in rhs]
        nodes = [x for x in left.nodes if x.id in intersection]
        Clique.__init__(self, nodes)
        self.left = left
        self.right = right

    @property
    def cost(self):
        return self.get_cost()

    @property
    def mass(self):
        return self.get_mass()

    def get_cost(self):
        return self.left.get_weight() + self.right.get_weight()

    def get_mass(self):
        return len(self.nodes)

    def __str__(self):
        return '|{}|'.format(str.join(',', [node.variable.name for node in self.nodes]))
