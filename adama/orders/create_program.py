# -*- coding: utf-8 -*-

"""This script allows you to adding data to the listen file that contains
all the data for generating playlist
"""

import sys
import os
from optparse import make_option

from adama import BaseOrder, OrderError

class Order(BaseOrder):

    options = BaseOrder.options

    help = __doc__
    args = "project_path name"

    def __init__(self, commander, order):
        super(Order, self).__init__(commander)
        self.order = order

    def _lines(self):
        lines = []
        lines.append('#!/usr/bin/env python\n')
        lines.append('# -*- coding: utf-8 -*-\n')
        lines.append('\n')
        lines.append('import sys\n')
        lines.append('from adama.commander import sir_yes_sir\n')
        lines.append('\n')
        lines.append("if __name__ == '__main__':\n")
        lines.append("    sys.exit(sir_yes_sir())\n")
        return lines


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
            program.writelines(self._lines())

        return 0
