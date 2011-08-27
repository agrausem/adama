# -*- coding utf-8 -*-

"""
"""

import unittest
import sys
import os
import shutil

from adama import call_order
from adama.tests import TestBaseOrders, no_shell_printing
from adama.exceptions import AdamaError, OrderError


class TestCreateProgram(TestBaseOrders):
    """Tests the creating program with the adama order
    """

    def setUp(self):
        super(TestCreateProgram, self).setUp()
        self.destination = os.path.join(self.base_path, 'bin')

    def tearDown(self):
        del self.destination
        super(TestCreateProgram, self).tearDown()

    def _isfile(self, filename):
        return os.path.isfile(os.path.join(self.destination, filename))

    def test_no_arg(self):
        """No argument passed to the order
        """
        with self.assertRaises(OrderError) as order_error:
            call_order('adama', 'create_program')
        exception = order_error.exception
        assert exception.message == 'The create_program order has one required argument'

    def test_command_name(self):
        """Tests creating a command with a name defined
        """
        call_order('adama', 'create_program', self.module, name=self.command, pythonpath='/tmp', path=self.destination)
        self.assertTrue(self._isfile(self.command))
        self._remove_from_syspath()

    def test_no_command_name(self):
        """Tests creating a command with no name defined
        """
        call_order('adama', 'create_program', self.module, name='', pythonpath='/tmp', path=self.destination)
        self.assertTrue(self._isfile(self.module))
        self._remove_from_syspath()

    def test_in_syspath(self):
        """Tests searching module with no pythonpath add and module in syspath
        """
        self._add_to_syspath()
        call_order('adama', 'create_program', self.module, name=self.command, pythonpath='', path=self.destination)
        self.assertTrue(self._isfile(self.command))
        self._remove_from_syspath()

    def test_not_in_syspath(self):
        """Tests searching module with no pythonpath add and module not in syspath
        """
        self.assertRaises(OrderError, call_order, 'adama', 'create_program', self.module, name=self.command, pythonpath='', path=self.destination)


class TestCreateOrder(TestBaseOrders):
    """ Tests creating new orders with the adama order
    """

    def  _isfile(self, order_file):
        return os.path.isfile(os.path.join(self.orders_path, order_file))

    def test_no_arg(self):
        """No argument passed to the order
        """
        with self.assertRaises(OrderError) as order_error:
            call_order('adama', 'create_order')
        exception = order_error.exception
        assert exception.message == 'The create_order order has two required arguments'

    def test_no_orders_module(self):
        """The orders module is absent
        """
        shutil.rmtree(self.orders_path)
        call_order('adama', 'create_order', self.module, 'no_module', pythonpath='/tmp', name=self.command)
        self.assertTrue(self._isfile('no_module.py'))
        self._remove_from_syspath()

    def test_in_syspath(self):
        """Tests creating orders in a package that is present in syspath
        """
        self._add_to_syspath()
        call_order('adama', 'create_order', self.module, 'test', pythonpath='', name=self.command)
        self.assertTrue(self._isfile('test.py'))
        self._remove_from_syspath()

    def test_not_in_syspath(self):
        """Tests creating orders in a package that is not present in syspath
        """
        self.assertRaises(OrderError, call_order, 'adama', 'create_order', self.module, 'test', pythonpath='', name=self.command)


if __name__ == '__main__':
    unittest.main()
