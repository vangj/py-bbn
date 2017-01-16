from pybbn.graph.potential import PotentialUtil


class EvidenceCollector:
    def __init__(self, join_tree, start_clique):
        self.join_tree = join_tree
        self.start_clique = start_clique

    def start(self):
        self.start_clique.mark()
        for sep_set_id in self.join_tree.get_neighbors(self.start_clique.id):
            sep_set = self.join_tree.get_node(sep_set_id)
            for clique_id in self.join_tree.get_neighbors(sep_set_id):
                y = self.join_tree.get_node(clique_id)
                if not y.is_marked():
                    self.__walk__(self.start_clique, sep_set, y)

    def __walk__(self, x, s, y):
        y.mark()
        for sep_set_id in self.join_tree.get_neighbors(y.id):
            sep_set = self.join_tree.get_node(sep_set_id)
            for clique_id in self.join_tree.get_neighbors(sep_set_id):
                clique = self.join_tree.get_node(clique_id)
                if not clique.is_marked():
                    self.__walk__(y, sep_set, clique)
        PotentialUtil.pass_single_message(self.join_tree, y, s, x)

