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

    arg = ''
    help = ''
    options = ()

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

    def decrypt(self):
        """Parse command args and options
        """
        return self.decrypter.parse_args()

    def run(self, *args, **kwargs):
        """The implementation of the command or order comes here
        """
        raise NotImplementedError()

    def __call__(self, args):
        """Executes the command
        """
        options, args = self.decrypt()
        try:
            result = self.run(*args, **options.__dict__)
        except OrderError, e:
            sys.stderr.write(str(e))
            sys.exit(1)


class Commander(QG):
    """Program class
    """

    __orders = {}

    def __init__(self, command, module):
        super(Commander, self).__init__(command, module)

    @property
    def orders(self):
        """Lists the available orders
        """
        app_orders = '{0}.orders'.format(self.module)
        package = __import__(app_orders) if app_orders not in sys.modules \
            else sys.modules[app_orders]

        if not self.__orders:
            for name in find_orders(package.__path__[0]):
                subpackage = '{0}.{1}'.format(app_orders, name)
                if subpackage not in sys.modules:
                    __import__(subpackage)
                self.__orders[name] = sys.modules[subpackage].Order(
                    self.command, self.module)

        return self.__orders

    @property
    def decrypter(self):
        decrypter = super(Commander, self).decrypter
        epilog = """
Type '{0} help <order>' for help on a specific order.

Available orders:
{1}

"""
        decrypter.epilog = epilog.format(self.command,
            '\n'.join('  {0}'.format(order) for order in self.orders)
        )
        return decrypter

    def get_order(self, name):
        """Gives an order by name
        """
        return self.orders[name]

    def __getitem__(self, key):
        return self.get_order(key)

    def run(self, *args, **kwargs):
        """Bad use of command so we print usage
        """
        self.explanations()
        return 0


class BaseOrder(QG):
    """The base class of a program that needs an implementation
    to define a command
    """

    args = ''
    help = ''
    options = ()

    def __init__(self, command, module):
        super(BaseOrder, self).__init__(command, module)
        self.name = self.__class__.__module__.split('.')[-1] \

    def usage(self):
        """Usage of a command
        """
        return '%prog {0.name} [options] {0.args}'.format(self)
