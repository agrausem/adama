# -*- coding: utf-8 -*-

"""
adama.tests.test_searching_orders
=================================

    Test finding and getting orders from filesystem ans sys.path
"""

import unittest
import os
import shutil

from adama.tests import TestBaseOrders

from adama.commandment import Commander
from adama.utils import find_orders, is_package, is_file, is_module
from adama.exceptions import UnknownOrderError


class TestFileUtils(unittest.TestCase):
    """Testing utils function on file
    """

    def test_is_a_package(self):
        """Tests if a file defines a python package
        """
        my_package = '__init__.py'
        self.assertTrue(is_package(my_package))

    def test_is_not_a_package(self):
        """Tests if a file doesn't define a python package
        """
        my_module = 'my_module.py'
        self.assertFalse(is_package(my_module))

    def test_is_a_module(self):
        """Tests if a file is a python module
        """
        self.assertTrue(is_module('module', '.py'))

    def test_is_not_a_module(self):
        """Tests of a file is not a python module
        """
        self.assertFalse(is_module('file', '.txt'))
        self.assertFalse(is_module('__init__', '.py'))

    def test_is_a_file(self):
        """Tests if element on filesystem is a file
        """
        with open('/tmp/my_module.py', 'w') as module:
            module.write('I\'m a Python module')
        self.assertTrue(is_file('/tmp', 'my_module.py'))
        os.remove('/tmp/my_module.py')

    def test_is_not_a_file(self):
        """Tests if an element on filesystem is not a file
        """
        self.assertFalse(is_file('/tmp', 'my_other_module.py'))
        os.mkdir('/tmp/my_directory')
        self.assertFalse(is_file('/tmp', 'my_directory'))
        os.rmdir('/tmp/my_directory')


class TestFindOrders(TestBaseOrders):
    """Testing searching files that contains order in the right
    package of project root path
    """

    def test_finding_orders(self):
        """Finding files that don't start with '_' and that are python files
        in the orders package
        """
        self._create_orders('add.py', 'remove.py')
        self.assertItemsEqual(find_orders(self.base_path), ['add', 'remove'])

    def test_not_finding_orders(self):
        """No filename matching in package
        """
        self._create_orders("add", "remove", "_clean.py")
        self.assertTrue(not find_orders(self.base_path))

    def test_with_os_error(self):
        """Package does not exist
        """
        self.assertTrue(not find_orders(self.orders_path))


class TestGetOrders(TestBaseOrders):
    """Testing instanciation of found orders
    """

    def setUp(self):
        super(TestGetOrders, self).setUp()
        self._add_to_syspath()
        self.commander = Commander(self.module, command=self.command)

    def tearDown(self):
        self._remove_from_syspath()
        super(TestGetOrders, self).tearDown()
        del self.commander

    def test_get_orders(self):
        """Test getting orders
        """
        self._create_orders('add.py', 'remove.py')
        self.assertItemsEqual(self.commander.orders, ['add', 'remove'])
        self._create_orders('clear.py')
        self.assertItemsEqual(self.commander.orders, ['add', 'remove'])
        new_commander = Commander(self.module, command=self.command)
        self.assertItemsEqual(new_commander.orders, ['add', 'remove', 'clear'])

    def test_get_order(self):
        """Test getting one order
        """
        self._create_orders('clear.py')
        assert repr(self.commander['clear']) == '<Order: clear>'

    def test_get_not_existing_order(self):
        """Test if an error is raised when trying to get an order that doesn't
        exist
        """
        with self.assertRaises(UnknownOrderError) as error:
            clear = self.commander['clear']
            clear()
        the_error = error.exception
        self.assertEqual(the_error.number, 11)
        self.assertRegexpMatches(str(the_error),
            'The order "clear" doesn\'t exist')
        self.assertEqual(repr(the_error), '<UnknownOrderError: {0}>'\
            .format(self.command))


class TestNoOrderPackage(TestBaseOrders):
    """Testing getting orders when no order package is available
    """

    def setUp(self):
        super(TestNoOrderPackage, self).setUp()
        shutil.rmtree(self.orders_path)
        self._add_to_syspath()

    def tearDown(self):
        self._remove_from_syspath()
        super(TestNoOrderPackage, self).tearDown()

    def test_no_order_package(self):
        """No order package is already created
        """
        commander = Commander(self.module)
        self.assertTrue(not commander.orders)


if __name__ == "__main__":
    unittest.main()
