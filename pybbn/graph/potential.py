class Potential:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def get_matching_entry(self, entry):
        matches = [e for e in self.entries if e.matches(entry)]
        return matches


class PotentialEntry:
    def __init__(self):
        self.entries = dict()
        self.value = 1.0

    def add(self, id, value):
        self.entries[id] = value;
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
