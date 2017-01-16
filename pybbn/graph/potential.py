import itertools


class Potential:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)
        return self

    def get_matching_entry(self, entry):
        return [e for e in self.entries if e.matches(entry)]

    def __str__(self):
        return str.join('\n', [entry.__str__() for entry in self.entries])


class PotentialEntry:
    def __init__(self):
        self.entries = dict()
        self.value = 1.0

    def add(self, k, v):
        self.entries[k] = v;
        return self

    def matches(self, that):
        for k, v in that.entries.items():
            if k not in self.entries or v != self.entries[k]:
                return False
        return True

    def duplicate(self):
        entry = PotentialEntry()
        for k, v in self.entries.items():
            entry.add(k, v)
        entry.value = self.value
        return entry

    def __str__(self):
        arr = ['{}={}'.format(k, v) for k, v in self.entries.items()]
        s = str.join(',', arr)
        return '{}|{}'.format(s, self.value)


class PotentialUtil:
    @staticmethod
    def pass_single_message(join_tree, x, s, y):
        old_sep_set_potential = join_tree.potentials[s.id]
        y_potential = join_tree.potentials[y.id]

        new_sep_set_potential = PotentialUtil.marginalize_for(join_tree, x, s.nodes)
        join_tree.potentials[s.id] = new_sep_set_potential

        PotentialUtil.multiply(y_potential, PotentialUtil.divide(new_sep_set_potential, old_sep_set_potential))

    @staticmethod
    def marginalize_for(join_tree, clique, nodes):
        potential = PotentialUtil.get_potential_from_nodes(nodes)
        clique_potential = join_tree.potentials.get(clique.id)

        for entry in potential.entries:
            matched_entries = clique_potential.get_matching_entries(entry)
            entry.value = sum([matched_entry.value for matched_entry in matched_entries])

        return potential

    @staticmethod
    def normalize(potential):
        total = sum([entry.value for entry in potential.entries])
        for entry in potential.entries:
            d = entry.value / total
            entry.value = d
        return potential

    @staticmethod
    def divide(numerator, denominator):
        potential = Potential()
        for entry in numerator.entries:
            if len(denominator.entries) > 0:
                e = denominator.entries[0]
                d = 0.0 \
                    if PotentialUtil.is_zero(entry.value) or PotentialUtil.is_zero(e.value) \
                    else (entry.value / e.value)
                new_entry = entry.duplicate()
                new_entry.value = d
                potential.add_entry(new_entry)
        return potential

    @staticmethod
    def is_zero(d):
        return 0.0 == d

    @staticmethod
    def multiply(bigger, smaller):
        for entry in smaller.entries:
            for e in bigger.get_matching_entries(entry):
                d = e.value * entry.value
                e.value = d

    @staticmethod
    def get_potential(node, parents):
        potential = PotentialUtil.get_potential_from_nodes(PotentialUtil.merge(node, parents))
        for i in range(len(potential.entries)):
            prob = node.probs[i]
            potential.entries[i].value = prob
        return potential

    @staticmethod
    def get_potential_from_nodes(nodes):
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
        return [i for i in itertools.product(*lists)]

    @staticmethod
    def merge(node, parents):
        nodes = [parent for parent in parents]
        nodes.append(node)
        return nodes
