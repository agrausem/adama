# -*- coding utf-8 -*-

"""
"""

import unittest
import sys

from adama.tests import TestBaseOrders, no_shell_printing, encapsulate_test_with_syspath
from adama import sir_yes_sir, call_order
from adama.exceptions import UnknownOrderError


sir_yes_sir = no_shell_printing(sir_yes_sir)


class TestShellHelp(TestBaseOrders):
    """Tests the help message and the way they are displayed
    """

    def test_no_args(self):
        """
        """
        assert sir_yes_sir(module=self.module, argv=[self.command]) == 1

    def test_global_help(self):
        """
        """
        assert sir_yes_sir(module=self.module, argv=[self.command, 'help']) == 1

    @encapsulate_test_with_syspath('add.py')
    def test_order_help(self):
        """
        """
        assert sir_yes_sir(module=self.module, argv=[self.command, 'help', 'add']) == 1


class TestShellNoOrder(TestBaseOrders):
    """Tests executing an order that doesn't exist
    """

    def runTest(self):
        assert sir_yes_sir(module=self.module, argv=[self.command, 'clear']) == 11


class TestShellExcuteOrder(TestBaseOrders):
    """Tests executing an order
    """

    @encapsulate_test_with_syspath('add.py')
    def runTest(self):
        assert sir_yes_sir(module=self.module, argv=[self.command, 'add']) == 0


class TestDirectLaunchOrder(TestBaseOrders):
    """Tests executing orders in python scripts
    """

    def test_no_order(self):
        """No order created
        """
        self.assertRaises(UnknownOrderError, call_order, self.module, 'add')

    @encapsulate_test_with_syspath('add.py')
    def test_executing_order(self):
        """
        """
        assert call_order(self.module, 'add') == 0

if __name__ == '__main__':
    unittest.main()
