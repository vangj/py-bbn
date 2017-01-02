class Edge:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    @property
    def key(self):
        a = min(self.i.uid, self.j.uid)
        b = max(self.i.uid, self.j.uid)
        return "{}--{}".format(a, b)