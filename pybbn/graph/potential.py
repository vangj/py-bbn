import itertools


class Potential(object):
    """
    Potential.
    """

    def __init__(self):
        """
        Ctor.
        """
        self.entries = []

    def add_entry(self, entry):
        """
        Adds a PotentialEntry.
        :param entry: PotentialEntry.
        :return: This potential.
        """
        self.entries.append(entry)
        return self

    def get_matching_entries(self, entry):
        """
        Gets all potential entries matching the specified entry.
        :param entry: PotentialEntry.
        :return: Array of matching potential entries.
        """
        return [e for e in self.entries if e.matches(entry)]

    def __str__(self):
        return str.join('\n', [entry.__str__() for entry in self.entries])


class PotentialEntry(object):
    """
    Potential entry.
    """

    def __init__(self):
        """
        Ctor.
        """
        self.entries = dict()
        self.value = 1.0

    def add(self, k, v):
        """
        Adds a node id and its value.
        :param k: Node id.
        :param v: Value.
        :return: This potential entry.
        """
        self.entries[k] = v
        return self

    def matches(self, that):
        """
        Checks if this potential entry matches the specified one. A match is determined with all the keys
        and their associated values in the potential entry passed in matches this one.
        :param that: PotentialEntry.
        :return:
        """
        for k, v in that.entries.items():
            if k not in self.entries or v != self.entries[k]:
                return False
        return True

    def duplicate(self):
        """
        Duplicates this entry.
        :return: PotentialEntry.
        """
        entry = PotentialEntry()
        for k, v in self.entries.items():
            entry.add(k, v)
        entry.value = self.value
        return entry

    def __str__(self):
        arr = ['{}={}'.format(k, v) for k, v in self.entries.items()]
        s = str.join(',', arr)
        return '{}|{}'.format(s, self.value)


class PotentialUtil(object):
    """
    Potential util.
    """

    @staticmethod
    def pass_single_message(join_tree, x, s, y):
        """
        Single message pass from x -- s -- y (from x to s to y).
        :param join_tree: Join tree.
        :param x: Clique.
        :param s: Separation-set.
        :param y: Clique.
        """
        old_sep_set_potential = join_tree.potentials[s.id]
        y_potential = join_tree.potentials[y.id]

        new_sep_set_potential = PotentialUtil.marginalize_for(join_tree, x, s.nodes)
        join_tree.potentials[s.id] = new_sep_set_potential

        PotentialUtil.multiply(y_potential, PotentialUtil.divide(new_sep_set_potential, old_sep_set_potential))

    @staticmethod
    def marginalize_for(join_tree, clique, nodes):
        """
        Marginalizes the specified clique's potential over the specified nodes.
        :param join_tree: Join tree.
        :param clique: Clique.
        :param nodes: List of BBN nodes.
        :return: Potential.
        """
        potential = PotentialUtil.get_potential_from_nodes(nodes)
        clique_potential = join_tree.potentials.get(clique.id)

        for entry in potential.entries:
            matched_entries = clique_potential.get_matching_entries(entry)
            entry.value = sum([matched_entry.value for matched_entry in matched_entries])

        return potential

    @staticmethod
    def normalize(potential):
        """
        Normalizes the potential (make sure they sum to 1.0).
        :param potential: Potential.
        :return: Potential.
        """
        total = sum([entry.value for entry in potential.entries])

        if total != 0.0:
            for entry in potential.entries:
                d = entry.value / total
                entry.value = d

        return potential

    @staticmethod
    def divide(numerator, denominator):
        """
        Divides two potentials.
        :param numerator: Potential.
        :param denominator: Potential.
        :return: Potential.
        """
        potential = Potential()
        for i, entry in enumerate(numerator.entries):
            e = denominator.entries[i]
            d = 0.0 \
                if PotentialUtil.is_zero(entry.value) or PotentialUtil.is_zero(e.value) \
                else (entry.value / e.value)
            new_entry = entry.duplicate()
            new_entry.value = d
            potential.add_entry(new_entry)
        return potential

    @staticmethod
    def is_zero(d):
        """
        Checks if the specified value is 0.0.
        :param d: Value.
        :return: A boolean indicating if the value is zero.
        """
        return 0.0 == d

    @staticmethod
    def multiply(bigger, smaller):
        """
        Multiplies two potentials. Order matters.
        :param bigger: Bigger potential.
        :param smaller: Smaller potential.
        """
        for entry in smaller.entries:
            for e in bigger.get_matching_entries(entry):
                d = e.value * entry.value
                e.value = d

    @staticmethod
    def get_potential(node, parents):
        """
        Gets the potential associated with the specified node and its parents.
        :param node: BBN node.
        :param parents: Parents of the BBN node (that themselves are also BBN nodes).
        :return: Potential.
        """
        potential = PotentialUtil.get_potential_from_nodes(PotentialUtil.merge(node, parents))
        for i in range(len(potential.entries)):
            prob = node.probs[i]
            potential.entries[i].value = prob
        return potential

    @staticmethod
    def get_potential_from_nodes(nodes):
        """
        Gets a potential from a list of BBN nodes.
        :param nodes: Array of BBN nodes.
        :return: Potential.
        """
        lists = [node.variable.values for node in nodes]
        cartesian = PotentialUtil.get_cartesian_product(lists)
        potential = Potential()
        for values in cartesian:
            entry = PotentialEntry()
            for i in range(len(nodes)):
                entry.add(nodes[i].id, values[i])
            potential.add_entry(entry)
        return potential

    @staticmethod
    def get_cartesian_product(lists):
        """
        Gets the cartesian product of a list of lists of values. For example, if the list is
        [ ['on', 'off'], ['on', 'off'] ],
        then the result will be a list of the following.
        * [ 'on', 'on']
        * [ 'on', 'off' ]
        * [ 'off', 'on' ]
        * [ 'off', 'off' ]
        :param lists: List of list of values.
        :return: Cartesian product of values.
        """
        return [i for i in itertools.product(*lists)]

    @staticmethod
    def merge(node, parents):
        """
        Merges the nodes into one array.
        :param node: BBN node.
        :param parents: BBN parent nodes.
        :return: Array of BBN nodes.
        """
        nodes = [parent for parent in parents]
        nodes.append(node)
        return nodes
