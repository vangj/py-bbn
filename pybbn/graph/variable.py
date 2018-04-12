class Variable(object):
    """
    A variable.
    """

    def __init__(self, id, name, values):
        """
        :param id: Numeric identifier. e.g. 0
        :param name: Name. e.g. 'a'
        :param values: Array of values. e.g. ['on', 'off']
        """
        self.id = id
        self.name = name
        self.values = values
