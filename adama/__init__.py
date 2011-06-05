# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser

class OrderError(Exception):
    """
    """
    pass

class BaseOrder(object):
    """The base class of a program that needs an implementation
    to define a command
    """

    args = ''
    help = ''
    options = ()

    def __init__(self, commander):
        self.commander = commander

    def usage(self, order_name):
        """Usage of a command
        """
        usage = '%prog {0} [options] {1}'.format(order_name, self.args)
        if self.help:
            return '{0}\n\n{1}'.format(usage, self.help)
        else:
            return usage

    def get_parser(self, order_name):
        """Initialize the option and argument parser for
        a command
        """
        return OptionParser(prog=self.commander,
            usage=self.usage(order_name),
            option_list=self.options
        )

    def get_help(self, order_name):
        """Prints the help of a command
        """
        parser = self.get_parser(order_name)
        parser.print_help()

    def parse_args(self, args):
        """Parse the command args ans options as defined in the
        subclass implementation of the command
        """
        parser = self.get_parser(args[0])
        return parser.parse_args()

    def run(self):
        """The real implementation of the command comes here
        """
        raise NotImplementedError()

    def __call__(self, args):
        """Executes the command with args given
        """
        options, args = self.parse_args(args)
        try:
            result = self.run(*args, **options.__dict__)
        except OrderError, e:
            sys.stderr.write(str(e))
            sys.exit(1)
