# -*- coding: utf-8

import os
import sys

from ..commandment import OrderError


def get_template(name):
    """
    """
    template_path = os.path.join(
        os.path.dirname(__path__[0]), 'templates', '{0}.template'.format(name)
    )
    with open(template_path) as template:
        return template.read()


def get_module(module_name, path):
    """Adds a path to a pythonpath and imports and returns a module
    """
    if path and path not in sys.path:
        sys.path.append(path)
    return __import__(module_name)


def get_command(name, module):
    """Defines command's name if user doesn't
    """
    if not name:
        return module.__name__
    return name


def touch(filename, times=None):
    """Creates an empty file
    """
    with file(filename, 'a'):
        os.utime(filename, times)

