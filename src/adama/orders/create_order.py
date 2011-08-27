# -*- coding: utf-8 -*-

"""Create Order order
"""

import os
from optparse import make_option

from ..commandment import BaseOrder
from ..exceptions import OrderError
from . import get_template, get_module, get_command, touch


class Order(BaseOrder):
    """Creates an order for your application that will be launch with a command as a subcommand

Arguments:
  module    python module that contains or will contain the orders module
  name      name of the order
    """

    options = BaseOrder.options + ()

    description = __doc__.split('\n')[0].lower()
    args = "module name"

    def __init__(self):
        super(Order, self).__init__('adama', command='adama')

    def execute(self, *args, **options):
        if len(args) != 2:
            raise OrderError('The create_order order has two required arguments', self)

        # adds a path to pythonpath if options has been selected
        # and if it is not already there and returns a module
        try:
            module = get_module(args[0], options['pythonpath'])
        except ImportError as e:
            raise OrderError(str(e), self)
        name = args[1]

        # Constructs, searches and creates the orders path
        orders_path = os.path.join(module.__path__[0], 'orders')
        if not os.path.isdir(orders_path):
            os.mkdir(orders_path)
            # Makes order a python module
            touch(os.path.join(orders_path, '__init__.py'))

        # Defines the command name
        command_name = get_command(options['name'], module)

        # Defines the order filename
        name = name if os.path.splitext(name)[1] == '.py' \
            else '{0}.py'.format(name)
        order_path = os.path.join(orders_path, name)

        # Writes in file
        with open(order_path, "w") as order:
            order.write(get_template('order')\
                .format(module.__name__, command_name))

        return 0
