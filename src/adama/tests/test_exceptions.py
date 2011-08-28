# -*- coding utf-8 -*-

"""
adama.tests.test_exceptions
===========================

    Testing messages and raised exceptions in adama library
"""

import unittest

from adama import call_order
from adama.tests import no_shell_printing
from adama.exceptions import AdamaError, OrderError


class TestBaseException(unittest.TestCase):
    """Test the implementation of adama's base exception
    """

    def test_printer_implented(self):
        """Tests that calling printer and return value of base exception
        """
        base_exception = AdamaError('Base exception')
        # print_error should be implemented
        self.assertRaises(NotImplementedError, base_exception.print_error)
        assert no_shell_printing(base_exception)() == 1


class TestOrderError(unittest.TestCase):
    """Tests errors catched in execution of orders
    """

    def test_raising_order_error(self):
        """Tests that an error during an order execution raised an OrderError
        exception and checks the returned value, message and representation of
    an instance
        """
        with self.assertRaises(OrderError) as order_error:
            call_order('adama', 'create_program')
        exception = order_error.exception
        # error printed on shell
        assert exception.print_error() == 'The create_program order has one \
required argument\nUsage: adama create_program [options] module\n'
        #  representation
        assert repr(exception) == '<OrderError: create_program>'
        # returned value
        assert no_shell_printing(exception)() == 12


if __name__ == '__main__':
    unittest.main()
