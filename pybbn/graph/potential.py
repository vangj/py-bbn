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

