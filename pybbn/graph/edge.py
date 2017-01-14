class Edge:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    @property
    def key(self):
        a = min(self.i.id, self.j.id)
        b = max(self.i.id, self.j.id)
        return "{}--{}".format(a, b)
