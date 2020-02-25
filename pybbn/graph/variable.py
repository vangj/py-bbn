from copy import deepcopy


class Variable(object):
    """
    A variable.
    """

    def __init__(self, id, name, values):
        """
        Ctor.

        :param id: Numeric identifier. e.g. 0
        :param name: Name. e.g. 'a'
        :param values: Array of values. e.g. ['on', 'off']
        """
        self.id = id
        self.name = name
        self.values = values

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memodict={}):
        cls = self.__class__
        result = cls.__new__(cls)
        memodict[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memodict))
        return result

    def __str__(self):
        return '{}|{}|{}'.format(self.id, self.name, self.values)

    def to_dict(self):
        """
        Gets a JSON serializable dictionary representation.

        :return: Dictionary.
        """
        return {
            'id': self.id,
            'name': self.name,
            'values': self.values
        }
