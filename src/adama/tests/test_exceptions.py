# -*- coding utf-8 -*-

"""
"""

import unittest
import sys

from adama import call_order
from adama.tests import TestBaseOrders, no_shell_printing
from adama.exceptions import AdamaError, OrderError


class TestBaseException(unittest.TestCase):
    """Test the implementation of adama's base exception
    """

    def runTest(self):
        base_exception = AdamaError('Base exception')
        self.assertRaises(NotImplementedError, base_exception.print_error)
        assert no_shell_printing(base_exception)() == 1


class TestOrderError(unittest.TestCase):
    """Tests errors catched in execution of orders
    """

    def runTest(self):
        with self.assertRaises(OrderError) as order_error:
            call_order('adama', 'create_program')
        exception = order_error.exception
        assert exception.print_error() == 'The create_program order has one required argument\nUsage: adama create_program [options] module\n'
        assert repr(exception) == '<OrderError: create_program>'
        assert no_shell_printing(exception)() == 12


if __name__ == '__main__':
    unittest.main()
