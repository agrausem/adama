# -*- coding: utf-8 -*-

"""This script allows you to adding data to the listen file that contains
all the data for generating playlist
"""

import os
from optparse import make_option

from adama import BaseOrder, OrderError


class Order(BaseOrder):
    """
    """

    options = BaseOrder.options

    help = __doc__
    args = "project_path library_name order_name"

    def __init__(self, commander, order):
        super(Order, self).__init__(commander)
        self.order = order

    def _lines(self):
        lines = []
        lines.append('# -*- coding: utf-8 -*-\n')
        lines.append('\n')
        lines.append('from adama.commander import BaseOrder, OrderError\n')
        lines.append('\n\n')
        lines.append('class Order(BaseOrder):\n')
        lines.append('    """\n')
        lines.append('    """\n')
        lines.append('\n')
        lines.append('    options = BaseOrder.options + (\n')
        lines.append('        # options for order come here\n')
        lines.append('    )\n')
        lines.append('\n')
        lines.append('    help = \'help for the order (ex: __doc__)\'\n')
        lines.append('    args = \'args of the order (ex: [options] arg1 arg2 \'\n')
        lines.append('\n')
        lines.append('    def __init__(self, commander, order):\n')
        lines.append('        super(Order, self).__init__(commander)\n')
        lines.append('        self.order = order\n')
        lines.append('\n')
        lines.append('    def run(self, *args, **options):\n')
        lines.append('        # the logic of the order comes here\n')
        lines.append('        return 0\n')
        return lines

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
            order.writelines(self._lines())

        return 0
