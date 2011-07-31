# -*- coding: utf-8 -*-

"""Some utils functions and classes
"""

import os
from optparse import OptionParser


class AdamaOptionParser(OptionParser):
    """Adama own option parser
    """

    def format_epilog(self, formatter):
        """Initial format_epilog function stris newline
        """
        return self.epilog


VERSION = '0.2'


def get_version(command=''):
    if command:
        return '{0} {1}'.format(command, VERSION)
    return VERSION


def find_orders(path):
    """
    """
    order_path = os.path.join(path, 'orders')
    try:
        return [order[:-3] for order in os.listdir(order_path)
            if not order.startswith('_') and order.endswith('.py')]
    except OSError:
        return []
