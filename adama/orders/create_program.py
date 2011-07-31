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

    options = BaseOrder.options

    help = __doc__
    args = "project_path name"

    def __init__(self, commander, module):
        super(Order, self).__init__(commander, module)

    def run(self, *args, **options):
        if len(args) != 3:
            raise OrderError('The create_program needs two arguments')

        project_path = args[1]
        prog_name = args[2]

        if not os.path.isdir(project_path):
            raise OrderError(
                'The project {0} does not exist'.format(project_path)
            )

        bin_path = os.path.join(project_path, 'bin')
        if not os.path.isdir(bin_path):
            os.mkdir(bin_path)

        script_path = os.path.join(bin_path, prog_name)

        with open(script_path, "w") as program:
            program.write(get_template('program'))

        return 0
