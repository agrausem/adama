# -*- coding: utf-8 -*-

"""
"""

import sys
import os
from optparse import NO_DEFAULT

from . import BaseOrder, OrderError

_orders = {}


def find_orders(path):
    """
    """
    order_path = os.path.join(path, 'orders')
    try:
        return [order[:-3] for order in os.listdir(order_path)
            if not order.startswith('_') and order.endswith('.py')]
    except OSError:
        return []


def get_orders(commander):
    """
    """
    global _orders

    app_orders = '{0}.orders'.format(commander)
    package = __import__(app_orders) \
        if app_orders not in sys.modules \
        else sys.modules[app_orders]

    if not _orders:
        for name in find_orders(package.__path__[0]):
            subpackage = '{0}.{1}'.format(app_orders, name)
            if subpackage not in sys.modules:
                __import__(subpackage)
            _orders[name] = sys.modules[subpackage].Order(commander)
    return _orders


def execute_order(commander, name, *args, **options):
    """
    """
    try:
        order = get_orders(commander)[name]
    except KeyError:
        raise OrderError, "Unknow order: {0}".format(name)

    defaults = dict([
        (option.dest, option.default) for option in order.option_list
        if option.default is not NO_DEFAULT
    ])
    defaults.update(options)

    return order(args, defaults)


def main_help(commander):
    """
    """
    options = BaseOrder(commander).options
    orders = get_orders(commander)

    helper = "Commander {0} help\n".format(commander)
    helper += 'usage: {0} order [options] [args]\n'.format(commander)
    helper += '\n'
    if options:
        helper += 'Options:\n'
        helper += '\n'.join(option for option in options)
    helper += "Type '{0} help <order>' for help on a specific order\n\n"\
        .format(commander)
    helper += "Available orders :\n"
    helper += '\n'.join('  {0}'.format(order) for order in orders)
    helper += '\n\n'

    sys.stdout.write(helper)

def sir_yes_sir(argv=None):
    """
    """
    argv = argv if argv else sys.argv[:]
    commander = os.path.basename(argv[0])

    no_arg = len(argv) == 1
    needs_help = not no_arg and argv[1] == 'help'
    global_help = needs_help and len(argv) == 2
    order_help = needs_help and len(argv) > 2

    if no_arg or global_help:
        main_help(commander)
        return 0
    else:
        order_name = argv[1] if not order_help else argv[2]
        try:
            order = get_orders(commander)[order_name]
        except OrderError as e:
            pass
        else:
            if order_help:
                order.get_help()
                return 0
            else:
                return order(argv[1:])
