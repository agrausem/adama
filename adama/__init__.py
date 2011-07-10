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
        self.order_name = self.__class__.__module__.split('.')[-1]

    def usage(self):
        """Usage of a command
        """
        usage = '%prog {0} [options] {1}'.format(self.order_name, self.args)
        if self.help:
            return '{0}\n\n{1}'.format(usage, self.help)
        else:
            return usage

    def get_parser(self):
        """Initialize the option and argument parser for
        a command
        """
        return OptionParser(prog=self.commander,
            usage=self.usage(),
            option_list=self.options
        )

    def get_help(self):
        """Prints the help of a command
        """
        parser = self.get_parser()
        parser.print_help()

    def parse_args(self):
        """Parse the command args and options as defined in the
        subclass implementation of the command
        """
        parser = self.get_parser()
        return parser.parse_args()

    def run(self):
        """The real implementation of the command comes here
        """
        raise NotImplementedError()

    def __call__(self, args):
        """Executes the command with args given
        """
        options, args = self.parse_args()
        try:
            result = self.run(*args, **options.__dict__)
        except OrderError, e:
            sys.stderr.write(str(e))
            sys.exit(1)
