# -*- coding: utf-8 -*-

"""
"""

import sys
import os

from .commandment import Commander, QG
from .exceptions import UnknownOrderError


VERSION = ('0', '3', '2', 'beta')


def get_version(command=''):
    version = '.'.join(element for element in VERSION[:3])
    return '{0} {1}'.format(command, version) if command else version


def sir_yes_sir(module='', doc='', options=(), version='', argv=None):
    """Launches the right order or displaying the help for a command or an order
    directly from command line.
    """
    argv = argv if argv is not None else sys.argv[:]
    command = os.path.basename(argv[0])
    module = module if module else command
    commander = Commander(module, doc=doc, command=command)

    # global options and app version made available for the orders
    QG.options = options
    QG.version = version

    no_arg = len(argv) == 1
    needs_help = not no_arg and argv[1] == 'help'
    global_help = needs_help and len(argv) == 2
    order_help = needs_help and len(argv) > 2

    if no_arg or global_help:
        return commander.explanations()
    else:
        order_name = argv[1] if not order_help else argv[2]
        try:
            order = commander[order_name]
        except UnknownOrderError as uoe:
            return uoe()
        else:
            if order_help:
                return order.explanations()
            else:
                return order(argv[2:])

def call_order(module_name, order_name, *args, **kwargs):
    """Calls an order from another python script directly
    """
    commander = Commander(module_name)
    order = commander[order_name]
    return order.execute(*args, **kwargs)
