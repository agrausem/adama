# -*- coding: utf-8 -*-

import sys

from .utils import find_orders, get_version, AdamaOptionParser


class OrderError(Exception):
    """
    """
    pass



class QG(object):
    """Base class for the adama library
    """

    args = ''
    options = ()
    examples = ''

    def __init__(self, command, module):
        self.command = command
        self.module = module

    def usage(self):
        """Usage of the command
        """
        return 'Usage: %prog order [options] [args]'

    @property
    def decrypter(self):
        """Gives the parser
        """
        return AdamaOptionParser(prog=self.command, usage=self.usage(),
            description=self.__doc__, option_list=self.options,
            version=get_version(command=self.command), epilog='')

    def explanations(self):
        """Help on command
        """
        self.decrypter.print_help()
        return 1

    def decrypt(self):
        """Parse command args and options
        """
        return self.decrypter.parse_args()

    def execute(self, *args, **kwargs):
        """The implementation of the command or order comes here
        """
        raise NotImplementedError()

    def __call__(self, args):
        """Executes the command
        """
        options, args = self.decrypt()
        try:
            result = self.execute(args, options)
        except OrderError, e:
            sys.stderr.write(str(e))
            sys.exit(1)


class Commander(QG):
    """Program class
    """

    __orders = {}

    def __init__(self, command, module, doc):
        super(Commander, self).__init__(command, module)
        self.doc = doc if doc else __doc__

    @property
    def orders(self):
        """Lists the available orders
        """
        app_orders = '{0}.orders'.format(self.module)
        try:
            package = __import__(app_orders) if app_orders not in sys.modules \
                else sys.modules[app_orders]
        except ImportError as e:
            print('The "orders" module can not be found under the {0} package'\
                .format(self.module))
        else:
            if not self.__orders:
                print package
                for name in find_orders(package.__path__[0]):
                    subpackage = '{0}.{1}'.format(app_orders, name)
                    if subpackage not in sys.modules:
                        __import__(subpackage)
                    self.__orders[name] = sys.modules[subpackage].Order(
                        self.command, self.module)

        return self.__orders

    @property
    def decrypter(self):
        """Adds epilog and doc informations to the command option parser
        """
        decrypter = super(Commander, self).decrypter

        # Adds doc to description of option parser
        decrypter.description = self.doc

        # Adds available orders or help creating orders to the epilog of option
        # parser
        epilog = """
Type '{0} help <order>' for help on a specific order.

Available orders:
{1}

"""
        if self.orders:
            # Returns the longest line length that will be printed on terminal
            max_ordername_len = max((len(name) for name in self.orders))
            # Pretty output of available orders
            available_orders = '\n'.join(
                '  {0:{2}}\t{1}'.format(name, order.description, max_ordername_len)
                for name, order in self.orders.items())
        else:
            # Help output when no orders can be found under package
            available_orders = """
No orders available.
Type 'adama create_order [options] {0} <order_name>' to create one"""\
                .format(self.module)
        # Formats the epilog
        decrypter.epilog = epilog.format(self.command, available_orders)

        return decrypter

    def get_order(self, name):
        """Gives an order by name
        """
        return self.orders[name]

    def __getitem__(self, key):
        return self.get_order(key)

    def execute(self, args, options):
        """Bad use of command so we print usage
        """
        return self.explanations()


class BaseOrder(QG):
    """The base class of a program that needs an implementation
    to define a command
    """

    def __init__(self, command, module):
        super(BaseOrder, self).__init__(command, module)
        self.name = self.__class__.__module__.split('.')[-1] \

    def usage(self):
        """Usage of a command
        """
        return '%prog {0.name} [options] {0.args}'.format(self)

    @property
    def decrypter(self):
        decrypter = super(BaseOrder, self).decrypter
        decrypter.epilog = self.examples
        return decrypter
