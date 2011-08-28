# -*- coding utf-8 -*-

"""
adama.tests.test_parsing_args
=============================

    Testing the capability of the library to parse and deal with arguments
    and options : showing help, direct launch, launching through command line,
    dealing with problem and exception

"""

import unittest

from adama.tests import TestBaseOrders, no_shell_printing, \
    encapsulate_test_with_syspath
from adama import sir_yes_sir, call_order
from adama.exceptions import UnknownOrderError


# disables the standard output printing
_sir_yes_sir = no_shell_printing(sir_yes_sir)


class TestShellHelp(TestBaseOrders):
    """Tests the help message and the way they are displayed
    """

    def test_no_args(self):
        """No argument shell return
        """
        assert _sir_yes_sir(module=self.module, argv=[self.command]) == 1

    def test_global_help(self):
        """Global help shell return
        """
        assert _sir_yes_sir(module=self.module, argv=[self.command, 'help']) \
            == 1

    @encapsulate_test_with_syspath('add.py')
    def test_order_help(self):
        """Order help shell return
        """
        assert _sir_yes_sir(module=self.module, argv=[self.command, 'help',
            'add']) == 1


class TestShellNoOrder(TestBaseOrders):
    """Tests executing an order that doesn't exist
    """

    # disables the standard output printing
    _sir_yes_sir = no_shell_printing(_sir_yes_sir)

    def test_no_order_found(self):
        """Order launched not found shell return
        """
        assert _sir_yes_sir(module=self.module, argv=[self.command, 'clear']) \
            == 11


class TestShellExcuteOrder(TestBaseOrders):
    """Tests executing an order
    """

    @encapsulate_test_with_syspath('add.py')
    def test_order_execution(self):
        """Order executed shell return
        """
        assert _sir_yes_sir(module=self.module, argv=[self.command, 'add']) \
            == 0


class TestDirectLaunchOrder(TestBaseOrders):
    """Tests executing orders in python scripts
    """

    def test_no_order(self):
        """No order found raises an exception
        """
        self.assertRaises(UnknownOrderError, call_order, self.module, 'add')

    @encapsulate_test_with_syspath('add.py')
    def test_executing_order(self):
        """Order executed function return
        """
        assert call_order(self.module, 'add') == 0


if __name__ == '__main__':
    unittest.main()
