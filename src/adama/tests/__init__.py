# -*- coding: utf-8 -*-

"""
adama.tests
===========

    Unit tests for the adama library.
"""

import unittest
import os
import sys
import shutil

from adama.commandment import QG
from adama.exceptions import AdamaError


class TestBaseOrders(unittest.TestCase):
    """Base test initializer
    """

    def setUp(self):
        self.base_path = '/tmp/pyproject'
        self.orders_path = self.base_path + '/orders'
        self.module = 'pyproject'
        self.command = 'pyp'
        # Creating temporary directories
        os.makedirs(self.orders_path)
        # Making packages
        for path in (self.base_path, self.orders_path):
            filename = os.path.join(path, '__init__.py')
            with file(filename, 'a'):
                os.utime(filename, None)

    def tearDown(self):
        # Removing temporary files
        shutil.rmtree(self.base_path)
        # Removing attributes
        del self.base_path
        del self.orders_path
        del self.module
        del self.command

    def _create_orders(self, *orders):
        """Creating some empty orders module"""
        orders_template_path = os.path.join(
            __import__('adama').__path__[0],
            'templates',
            'order.template'
        )
        with open(orders_template_path, 'r') as template:
            order = template.read().format(self.module, self.command)
            for filename in orders:
                with open(os.path.join(self.orders_path, filename), 'a') \
                    as new_order:
                    new_order.write(order)

    def _add_to_syspath(self):
        """Adds a path to sys.path"""
        sys.path.append(os.path.dirname(self.base_path))

    def _remove_from_syspath(self):
        """Removes a path to sys.path and modules from sys.modules"""
        for mod in [mod for mod in sys.modules if mod.startswith(self.module)]:
            del sys.modules[mod]
        sys.path.remove(os.path.dirname(self.base_path))


def no_shell_printing(func):
    """No shell printing for help when lauching tests
    """
    print_functions = (QG.explanations, AdamaError.__call__)

    def wrap(**kwargs):
        """Wrapper for the printing function"""
        for function in print_functions:
            function.im_func.func_defaults = (False, )
        result = func(**kwargs)
        for function in print_functions:
            function.im_func.func_defaults = (True, )
        return result

    return wrap


def encapsulate_test_with_syspath(*orders):
    """Creates orders, adds path to sys path before launching test
    and removes path and modules
    """
    def wrap(func):
        """Wrapper for calling a function in a package that needs to be in
        sys.path"""
        def wrapped_f(instance, *args, **kwargs):
            """Adding in sys.path, launching func and remove from sys.path"""
            instance._create_orders(*orders)
            instance._add_to_syspath()
            func(instance, *args, **kwargs)
            instance._remove_from_syspath()
        return wrapped_f
    return wrap
