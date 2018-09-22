import itertools

import numpy as np


class DiscreteData(object):
    """
    A discrete dataset.
    """
    def __init__(self, df):
        """
        Ctor.
        :param df: Dataframe.
        """
        self.df = df
        if self.__is_valid__() is False:
            raise Exception('Data is not valid.')
        self.variable_profiles = self.get_variable_profiles()
        self.N = df.shape[0]
        self.probs = {}
        self.counts = {}

    def get_variables(self, by_name=True):
        """
        Gets a dictionary of variables. Keys could be the name or numeric id.
        :param by_name: A boolean indicating if keys should be names or not. True by default.
        :return: Dictionary.
        """
        variables = {}
        for i, col in enumerate(self.df.columns):
            if by_name is True:
                variables[col] = i
            else:
                variables[i] = col
        return variables

    def get_variable_profiles(self):
        """
        Gets a dictionary of values for each variable. Keys are variable/column names and values are list
        of the domain/values of the variable.
        :return: Dictionary.
        """
        profile = {}
        for col in self.df.columns:
            s = self.df[col].value_counts()
            profile[col] = list(s.index)
        return profile

    def __is_valid__(self):
        """
        Checks to see if the dataframe is valid. Each variable/column must have more than 1 unique (at least 2) values.
        :return: Boolean indicating if the data is valid.
        """
        valid = True
        for col in self.df.columns:
            s = self.df[col].value_counts()
            if len(s) < 2:
                valid = False
                break
        return valid

    def __sort__(self, names, vals):
        """
        Sorts the names and corresponding values ascendingly by name.
        :param names: List of names.
        :param vals: List of values.
        :return: List of tuple, where each tuple is a (name, value).
        """
        pairs = [(n, v) for n, v in zip(names, vals)]
        pairs = sorted(pairs, key=lambda t: t[0])
        return pairs

    def __to_query__(self, names, vals):
        """
        Converts the names and corresponding values to a query filter. For example, if names = ['a', 'c', 'b']
        and values = ['true', 'false', 'true'], then a filter is generated as follows, 'a == "true" and b == "true"
        and c == "false"'.
        :param names: List of names.
        :param vals: List of values.
        :return: Query filter for use with dataframe.query(...) method.
        """
        pairs = self.__sort__(names, vals)
        pairs = ' and '.join(['{} == "{}"'.format(t[0], t[1]) for t in pairs])
        return pairs

    def __count__(self, names, vals):
        """
        Counts the frequency of the combination of the specified values.
        :param names: Names of variables.
        :param vals: Values of variables.
        :return: Count.
        """
        q = self.__to_query__(names, vals)
        if q in self.counts:
            return self.counts[q]
        else:
            n = self.df.query(q).shape[0]
            self.counts[q] = n
            return self.counts[q]

    def __count_parents_child__(self, ch_name, ch_val, pa_names, pa_vals):
        """
        Counts the frequency of the specified combination of parent and child values.
        :param ch_name: Child name.
        :param ch_val: Child value.
        :param pa_names: Parent name.
        :param pa_vals: Parent value.
        :return: Count.
        """
        names = [ch_name]
        names.extend(pa_names)

        vals = [ch_val]
        vals.extend(pa_vals)

        return self.__count__(names, vals)

    def __get_prob__(self, name, val):
        """
        Gets the probability of a variable equal to the specified value.
        :param name: Name of variable/column.
        :param val: Value.
        :return: Probability, P(name = val).
        """
        q = '{} == "{}"'.format(name, val)
        if q in self.probs:
            return self.probs[q]

        n = self.df.query(q).shape[0]
        p = n / float(self.N)
        self.probs[q] = p
        return p

    def __get_joint_prob__(self, name1, val1, name2, val2):
        """
        Gets the joint probability of two variables equal to the corresponding values.
        :param name1: Name of variable/column.
        :param val1: Value of variable.
        :param name2: Name of variable/column.
        :param val2: Value of variable.
        :return: Probability, P(name1 = val1, name2 = val2).
        """
        q = self.__to_query__([name1, name2], [val1, val2])
        if q in self.probs:
            return self.probs[q]

        n = self.df.query(q).shape[0]
        p = n / float(self.N)
        self.probs[q] = p
        return p

    def __get_joint_prob_set__(self, name1, val1, cond_names, cond_vals):
        """
        Gets the joint probability of a variable given a set of variables.
        :param name1: Name of variable/column.
        :param val1: Value of variable.
        :param cond_names: List of names of variables/columns.
        :param cond_vals: List of values of variables.
        :return: Joint probability, P(name1 = val1, cond_names = cond_vals).
        """
        # compute P(x_i, x_k)
        names = [name1]
        names.extend(cond_names)

        vals = [val1]
        vals.extend(cond_vals)

        q_ik = self.__to_query__(names, vals)
        p_ik = None

        if q_ik in self.probs:
            p_ik = self.probs[q_ik]
        else:
            n = self.df.query(q_ik).shape[0]
            p = n / float(self.N)
            self.probs[q_ik] = p
            p_ik = self.probs[q_ik]

        return p_ik

    def __get_joint_prob_triplet__(self, name1, val1, name2, val2, cond_names, cond_vals):
        """
        Gets the joint probability of three variables equal to the corresponding values. Note that the last
        two parameters should be a list of variable names and values.
        :param name1: Name of variable/column.
        :param val1: Value of variable.
        :param name2: Name of variable/column.
        :param val2: Value of variable.
        :param cond_names: List of names of variables/columns.
        :param cond_vals: List of values of variables.
        :return: Probability, P(name1 = val1, name2 = val2, cond_names = cond_vals).
        """
        # compute P(x_i, x_j, x_k)
        names = [name1, name2]
        names.extend(cond_names)

        vals = [val1, val2]
        vals.extend(cond_vals)

        q_ijk = self.__to_query__(names, vals)
        p_ijk = None

        if q_ijk in self.probs:
            p_ijk = self.probs[q_ijk]
        else:
            n = self.df.query(q_ijk).shape[0]
            p = n / float(self.N)
            self.probs[q_ijk] = p
            p_ijk = self.probs[q_ijk]

        return p_ijk

    def __get_cond_prob__(self, name1, val1, name2, val2):
        """
        Gets the conditional probability of two variables, namely, P(name1 | name2).
        :param name1: Name of variable/column.
        :param val1: Value of variable.
        :param name2: Name of variable/column.
        :param val2: Value of variable.
        :return: Conditional probability, P(name1 = val1 | name2 = val2).
        """
        p_ij = self.__get_joint_prob__(name1, val1, name2, val2)
        p_j = self.__get_prob__(name2, val2)
        p_i_j = p_ij / p_j
        return p_i_j

    def __get_cond_prob_set__(self, name1, val1, cond_names, cond_vals):
        """
        Gets the conditional probability of a variable given a set of variables, namely, P(name1 | cond_names).
        :param name1: Name of variable/column.
        :param val1: Value of variable.
        :param cond_names: List of names of variables/columns.
        :param cond_vals: List of values of variables.
        :return: Conditional probability, P(name1 = val1 | cond_names = cond_vals).
        """
        # compute P(x_i, x_k)
        p_ik = self.__get_joint_prob_set__(name1, val1, cond_names, cond_vals)

        # compute P(x_k)
        q_k = self.__to_query__(cond_names, cond_vals)
        p_k = None

        if q_k in self.probs:
            p_k = self.probs[q_k]
        else:
            n = self.df.query(q_k).shape[0]
            p = n / float(self.N)
            self.probs[q_k] = p
            p_k = self.probs[q_k]

        try:
            p_i_k = p_ik / p_k
        except ZeroDivisionError:
            p_i_k = 0.0

        return p_i_k

    def __get_cond_prob_triplet__(self, name1, val1, name2, val2, cond_names, cond_vals):
        """
        Gets the conditional probability of two variables given a set of third variables, namely,
        P(name1, name2 | cond_names).
        :param name1: Name of variable/column.
        :param val1: Value of variable.
        :param name2: Name of variable/column.
        :param val2: Value of variable.
        :param cond_names: List of names of variables/columns.
        :param cond_vals: List of values of variables.
        :return: Conditional probability, P(name1 = val1, name2 = val2 | cond_names = cond_vals).
        """
        # compute P(x_i, x_j, x_k)
        p_ijk = self.__get_joint_prob_triplet__(name1, val1, name2, val2, cond_names, cond_vals)

        # compute P(x_k)
        q_k = self.__to_query__(cond_names, cond_vals)
        p_k = None

        if q_k in self.probs:
            p_k = self.probs[q_k]
        else:
            n = self.df.query(q_k).shape[0]
            p = n / float(self.N)
            self.probs[q_k] = p
            p_k = self.probs[q_k]

        try:
            p_ij_k = p_ijk / p_k
        except ZeroDivisionError:
            p_ij_k = 0.0

        return p_ij_k

    def __get_mi__(self, name1, name2):
        """
        Gets the mutual information between two variables.
        :param name1: Name of variable/column.
        :param name2: Name of variable/column.
        :return: Mutual information, I(name1, name2).
        """
        vals1 = self.variable_profiles[name1]
        vals2 = self.variable_profiles[name2]

        mi = 0.0
        for val1 in vals1:
            p_i = self.__get_prob__(name1, val1)
            for val2 in vals2:
                p_j = self.__get_prob__(name2, val2)
                p_ij = self.__get_joint_prob__(name1, val1, name2, val2)

                if p_i != 0.0 and p_j != 0.0:
                    x = p_ij / p_i / p_j

                    if x == 0.0:
                        pass
                    else:
                        weight = np.log(x)
                        mi += p_ij * weight
        return mi

    def __get_cond_mi__(self, name1, name2, cond_names):
        """
        Gets the conditional mutual information between two variables given a third set of variables.
        :param name1: Name of variable/column.
        :param name2: Name of variable/column.
        :param cond_names: List of names of variables/columns.
        :return: Conditional mutual information, I(name1, name2 | cond_names).
        """
        vals1 = self.variable_profiles[name1]
        vals2 = self.variable_profiles[name2]
        vals = list(itertools.product(*[self.variable_profiles[name] for name in cond_names]))

        mi = 0.0

        for val1 in vals1:
            for val2 in vals2:
                for cond_vals in vals:
                    p_ijk = self.__get_joint_prob_triplet__(name1, val1, name2, val2, cond_names, cond_vals)
                    p_ij_k = self.__get_cond_prob_triplet__(name1, val1, name2, val2, cond_names, cond_vals)
                    p_i_k = self.__get_cond_prob_set__(name1, val1, cond_names, cond_vals)
                    p_j_k = self.__get_cond_prob_set__(name2, val2, cond_names, cond_vals)

                    if p_i_k != 0.0 and p_j_k != 0.0:
                        x = p_ij_k / p_i_k / p_j_k

                        if x == 0.0:
                            pass
                        else:
                            weight = np.log(x)
                            mi += p_ijk * weight

        return mi

    def __factorial__(self, x):
        if x <= 0.0:
            return 1

        # typically stirling's approximation would be (x / e)^x
        # for large values of x, this creates an overflow
        # we use 1 here, which doesn't seem to affect the sampling or probability estimations
        g = np.sqrt(2 * np.pi * x) * np.power(x / 2.718281, 1)
        return g

    def __gamma__(self, n):
        return self.__factorial__(n - 1)

    def is_cond_dep(self, name1, name2, names):
        """
        Checks if two variables are conditionally dependent give a third set of variables.
        :param name1: Name of variable/column.
        :param name2: Name of variable/column.
        :param names: List of names of variables/columns.
        :return: A tuple, (conditional mutual information, boolean), to signal if two variables are
        conditionally dependent.
        """
        mi = self.__get_mi__(name1, name2)
        cmi = self.__get_cond_mi__(name1, name2, names)
        if cmi > mi:
            return cmi, True
        return cmi, False

    def get_pairwise_mutual_information(self):
        """
        Gets all unique pairwise mutual information.
        :return: List of tuples where each tuple is (name1, name2, mi).
        """
        mis = []
        variables = sorted(list(self.variable_profiles.keys()))
        for i in range(len(variables)):
            name1 = variables[i]
            for j in range(len(variables)):
                name2 = variables[j]
                if j > i:
                    mi = self.__get_mi__(name1, name2)
                    t = (name1, name2, mi)
                    mis.append(t)
        mis = sorted(mis, key=lambda t: t[2], reverse=True)
        return mis

    def get_local_kutato(self, child, parents):
        """
        Computes the local K2 (Kutato) score of a child and its parents.
        See https://www.cs.waikato.ac.nz/~remco/weka.bn.pdf. The score is converted
        to its log form to avoid numerical overflow. All scores should be negative,
        with scores closer to zero indicating better likelihood (higher scores
        indicate the parent-child relationship is more likely).
        :param child: Child.
        :param parents: Parent.
        :return: Log of the K2 score.
        """
        r_i = len(self.variable_profiles[child])
        gamma_r_i = self.__gamma__(r_i)

        q_i = list(itertools.product(*[self.variable_profiles[parent] for parent in parents]))

        log_score = 0.0

        for vals in q_i:
            N_ij = self.__count__(parents, vals)
            gamma_N_ij = self.__gamma__(r_i + N_ij)

            log_sum = np.log(gamma_r_i) - np.log(gamma_N_ij)

            for val in self.variable_profiles[child]:
                N_ijk = self.__count_parents_child__(child, val, parents, vals)
                factorial_N_ijk = self.__factorial__(N_ijk)
                log_sum += np.log(factorial_N_ijk)

            log_score += log_sum

        return log_score
