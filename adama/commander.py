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
            _orders[name] = sys.modules[subpackage]
    return _orders


def execute_order(commander, name, *args, **options):
    """
    """
    try:
        order = get_orders(commander)[name].Order(commander, name)
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
    helper = "Usage of commander {0}:\n".format(commander)
    helper += '{0} order [options] args\n'.format(commander)
    helper += '\n'
    helper += "Available orders :\n"
    helper += 'help\n'
    helper += '\n'.join(order for order in get_orders(commander))
    helper += '\n\n'

    sys.stdout.write(helper)

def sir_yes_sir(argv=None):
    """
    """
    argv = argv if argv else sys.argv[:]
    commander = os.path.basename(argv[0])

    if len(argv) == 1:
        main_help(commander)
        return 0

    order = argv[1]

    if order == 'help':
        if len(argv) > 2:
            order = BaseOrder(commander)
            order.get_help(argv[2])
        else:
            main_help(commander)
        return 0

    try:
        order = get_orders(commander)[order].Order(commander, order)
    except OrderError as e:
        pass
    else:
        return order(argv[1:])

