# -*- coding: utf-8 -*-

"""Adama's exceptions declaration
"""


class AdamaError(Exception):
    """Base exception for adama
    """

    def __init__(self, msg, number=1):
        self.message = msg
        self.number = number

    def print_error(self):
        """Prints error in shell"""
        raise NotImplementedError

    def __str__(self):
        return self.message

    def __call__(self):
        print(self.print_error())
        return self.number


class UnknownOrderError(AdamaError):
    """
    """

    def __init__(self, msg, commander):
        super(UnknownOrderError, self).__init__(msg, 11)
        self.commander = commander

    def print_error(self):
        return '{0!s}\n\n{0.commander.available_orders}\n'\
            .format(self)

    def __str__(self):
        return self.message

    def __repr__(self):
        return '<UnknownOrderError: {0.commander.command}>'.format(self)


class OrderError(AdamaError):
    """
    """

    def __init__(self, msg, order):
        super(OrderError, self).__init__(msg, 12)
        self.order = order

    def print_error(self):
        return '{0!s}\n{0.order!s}\n'.format(self)

    def __repr__(self):
        return '<OrderError: {0.name}>'.format(self.order)
