# -*- coding: utf-8 -*-

"""Create Program Order
"""

import sys
import os
from optparse import make_option

from ..commandment import BaseOrder, OrderError
from . import get_module, get_template

class Order(BaseOrder):
    """Creates a command line program for your application that will look for orders

Argument:
  module      Python module that contains or will contain the orders module
    """

    options = BaseOrder.options + (
        make_option('-d', '--directory', action='store', type='string',
            dest='path', metavar='PATH', default=os.getcwd(),
            help='directory to save the command [Default: %default]'),
        make_option('-n', '--name', action='store', type='string', dest='name',
            metavar='NAME', help='name of the command [Default: module\'s name]'),
    )

    args = "module"
    description = __doc__.split('\n')[0].lower()
    examples = ""

    def __init__(self, commander, module):
        super(Order, self).__init__(commander, module)

    def execute(self, args, options):
        if len(args) != 2:
            raise OrderError('The create_program has one required argument',
                self.usage())

        module = get_module(args[1], options.pythonpath)

        # Checks if entered path exists and create it
        if not os.path.isdir(options.path):
            os.makedirs(options.path)

        # Defines command's name if user doesn't
        if not options.name:
            options.name = module.__name__.split('.')[-1]

        # Path to save the command
        file_path = os.path.join(options.path, options.name)

        # Writes data coming from template to file
        with open(file_path, "w") as program:
            template = get_template('program')
            program.write(template.format(module.__name__))

        return 0
