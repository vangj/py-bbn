import numpy as np


class DiscreteData(object):
    def __init__(self, df):
        self.df = df
        if self.__is_valid__() is False:
            raise Exception('Data is not valid.')
        self.variable_profiles = self.__get_variable_profiles__()
        self.N = df.shape[0]
        self.probs = {}

    def __get_variable_profiles__(self):
        profile = {}
        for col in self.df.columns:
            s = self.df[col].value_counts()
            profile[col] = list(s.values)
        return profile

    def __is_valid__(self):
        valid = True
        for col in self.df.columns:
            s = self.df[col].value_counts()
            if len(s) < 2:
                valid = False
                break
        return valid

    def __get_prob__(self, name, val):
        q = '{} == "{}"'.format(name, val)
        if q in self.probs:
            return self.probs[q]

        n = self.df.query(q).shape[0]
        p = n / float(self.N)
        self.probs[q] = p
        return p

    def __get_joint_prob__(self, name1, val1, name2, val2):
        lhs_name = name1 if name1 < name2 else name2
        lhs_value = val1 if name1 < name2 else val2
        rhs_name = name1 if lhs_name == name2 else name2
        rhs_value = val1 if lhs_name == name2 else val2

        q = '{} == "{}" and {} == "{}"'.format(lhs_name, lhs_value, rhs_name, rhs_value)
        if q in self.probs:
            return self.probs[q]

        n = self.df.query(q).shape[0]
        p = n / float(self.N)
        self.probs[q] = p
        return p

    def __get_mi__(self, name1, name2):
        vals1 = self.variable_profiles[name1]
        vals2 = self.variable_profiles[name2]

        mi = 0.0
        for val1 in vals1:
            p1 = self.__get_prob__(name1, val1)
            for val2 in vals2:
                p2 = self.__get_prob__(name2, val2)
                jp = self.__get_joint_prob__(name1, val1, name2, val2)

                try:
                    l = np.log(jp / p1 / p2)
                    if p1 * p2 == 0 or np.isinf(l):
                        pass
                    else:
                        mi += jp * l
                except ZeroDivisionError:
                    pass
        return mi

