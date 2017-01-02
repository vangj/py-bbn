class Node:
    def __init__(self, uid):
        self.uid = uid

    @property
    def key(self):
        return self.uid
