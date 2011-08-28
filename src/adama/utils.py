# -*- coding: utf-8 -*-

"""
adama.utils
===========

    The adama option parser that inherits OptionParser and utils function
    to check python package module and package and to find orders on filesystem
"""

import os
from optparse import OptionParser


class AdamaOptionParser(OptionParser):
    """Adama own option parser
    """

    def format_epilog(self, formatter):
        """Initial format_epilog function strips newline
        """
        return self.epilog

    def format_description(self, formatter):
        """Initial format_description function strips newline
        """
        return self.description


def is_package(filename):
    """ Checks if filename looks like a Python package
    """
    return filename.startswith('_')


def is_module(name, extension):
    """ Checks if file looks like a Python module
    """
    return not is_package(name + extension) and extension == '.py'


def is_file(path, element):
    """ Checks if an element from directory tree is a file
    """
    return os.path.isfile(os.path.join(path, element))


def find_orders(path):
    """Finds orders in filesystem given a path
    """
    default_order_directory = 'orders'
    # returns only python modules name found in orders path
    try:
        orders_path = os.path.join(path, default_order_directory)
        splitted_files = [os.path.splitext(element) for element
            in os.listdir(orders_path) if is_file(orders_path, element)]
        return [filename for filename, extension in splitted_files
            if is_module(filename, extension)]
    except OSError:
        return []
