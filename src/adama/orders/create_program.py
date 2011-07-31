# -*- coding: utf-8 -*-

"""This script allows you to adding data to the listen file that contains
all the data for generating playlist
"""

import sys
import os
from optparse import make_option

from adama.commandment import BaseOrder, OrderError
from adama.orders import get_template

class Order(BaseOrder):
    """Creates a program script that can launch orders from a python module

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
    examples = ""

    def __init__(self, commander, module):
        super(Order, self).__init__(commander, module)

    def run(self, args, options):
        if len(args) != 2:
            raise OrderError('The create_program has one required argument',
                self.usage())

        module = args[1]

        # Checks if entered path exists and create it
        if not os.path.isdir(options.path):
            os.makedirs(options.path)

        # Defines command's name if user doesn't
        if not options.name:
            options.name = module.split('.')[-1]

        # Path to save the command
        file_path = os.path.join(options.path, options.name)

        # Writes data coming from template to file
        with open(file_path, "w") as program:
            template = get_template('program')
            program.write(template.format(module))

        return 0
