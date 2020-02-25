from pybbn.graph.potential import PotentialUtil


class EvidenceDistributor(object):
    """
    Evidence distributor. Passes messages using breadth-first-search (BFS).
    Messages are passed from the start clique to the far remote cliques.
    """

    def __init__(self, join_tree, start_clique):
        """
        Ctor.

        :param join_tree: Join tree.
        :param start_clique: Start clique.
        """
        self.join_tree = join_tree
        self.start_clique = start_clique

    @staticmethod
    def __get_neighboring_cliques__(join_tree, clique):
        """
        Gets the neighboring cliques.
        :param join_tree: Join tree.
        :param clique: Clique.
        :return: Tuple. First tuple is list of neighboring sep-sets and second is list of neighboring cliques.
        """
        sepsets = []
        cliques = []

        sep_set_ids = join_tree.get_neighbors(clique.id)
        for sep_set_id in sep_set_ids:
            clique_ids = join_tree.get_neighbors(sep_set_id)
            for clique_id in clique_ids:
                t1 = (sep_set_id, join_tree.get_node(sep_set_id))
                t2 = (clique_id, join_tree.get_node(clique_id))
                if clique_id != clique.id:
                    sepsets.append(t1)
                    cliques.append(t2)

        return sepsets, cliques

    def start(self):
        """
        Starts the evidence distribution.
        """
        self.start_clique.mark()
        sepsets, cliques = self.__get_neighboring_cliques__(self.join_tree, self.start_clique)

        for clique in cliques:
            clique[1].mark()

        for s, c in zip(sepsets, cliques):
            PotentialUtil.pass_single_message(self.join_tree, self.start_clique, s[1], c[1])
            self.__walk__(self.start_clique, s[1], c[1])

    def __walk__(self, x, s, y):
        """
        Walks away from the specified node y.

        :param x: Clique.
        :param s: Separation-set.
        :param y: Clique.
        """
        sepsets, cliques = self.__get_neighboring_cliques__(self.join_tree, y)

        s_arr = []
        c_arr = []
        for sep, cli in zip(sepsets, cliques):
            if not cli[1].is_marked():
                cli[1].mark()
                s_arr.append(sep)
                c_arr.append(cli)

        for sep, cli in zip(s_arr, c_arr):
            PotentialUtil.pass_single_message(self.join_tree, y, sep[1], cli[1])
            self.__walk__(y, sep[1], cli[1])
