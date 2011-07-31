# -*- coding: utf-8 -*-

"""This script allows you to adding data to the listen file that contains
all the data for generating playlist
"""

import os
from optparse import make_option

from adama.commandment import BaseOrder, OrderError
from adama.orders import get_template

class Order(BaseOrder):
    """
    """

    options = BaseOrder.options

    help = __doc__
    args = "project_path library_name order_name"

    def __init__(self, commander, module):
        super(Order, self).__init__(commander, module)

    def run(self, *args, **options):
        if len(args) != 4:
            raise OrderError('The create_program needs three arguments')

        project_path = args[1]
        library_name = args[2]
        order_name = args[3]

        if not os.path.isdir(project_path):
            raise OrderError(
                'The project {0} does not exist'.format(project_path)
            )

        orders_path = os.path.join(project_path, library_name, 'orders')
        if not os.path.isdir(orders_path):
            os.mkdir(orders_path)

        if not order_name.endswith('.py'):
            order_name = '{0}.py'.format(order_name)
        order_path = os.path.join(orders_path, order_name)

        with open(order_path, "w") as order:
            order.write(get_template('order'))

        return 0
