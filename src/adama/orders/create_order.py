# -*- coding: utf-8 -*-

"""Create Order order
"""

import os
from optparse import make_option

from adama.commandment import BaseOrder, OrderError
from adama.orders import get_template, add_to_pythonpath


class Order(BaseOrder):
    """Creates an order for your application that will be launch with a command
as a subcommand

Arguments:
  module    python module that contains or will contain the orders module
  name      name of the order
    """

    options = BaseOrder.options + ()
    description = __doc__.split('\n')[0].lower()
    args = "module name"

    def __init__(self, commander, module):
        super(Order, self).__init__(commander, module)

    def execute(self, args, options):
        if len(args) != 3:
            raise OrderError('The create_program has 3 required arguments', self.usage())

        name = args[2]

        # adds a path to pythonpath if options has been selected
        # and if it is not already there
        add_to_pythonpath(options.pythonpath)

        try:
            module = __import__(args[1])
        except ImportError as e:
            raise OrderError(str(e))

        # Constructs, searches and creates the orders path
        orders_path = os.path.join(module.__path__[0], 'orders')
        if not os.path.isdir(orders_path):
            os.mkdir(orders_path)
            # Makes order a python module
            touch(os.path.join(orders_path, '__init__.py'))

        # Defines the order filename
        name = name if os.path.splitext(name)[1] == '.py' \
            else '{0}.py'.format(name)
        order_path = os.path.join(orders_path, name)

        # Writes in file
        with open(order_path, "w") as order:
            template = get_template('order')
            order.write(get_template('order'))

        return 0
