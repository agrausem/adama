# -*- coding: utf-8

import os
import sys

def get_template(name):
    """
    """
    template_path = os.path.join(
        os.path.dirname(__path__[0]), 'templates', '{0}.template'.format(name)
    )
    with open(template_path) as template:
        return template.read()

def add_to_pythonpath(path):
    """
    """
    if path and path not in sys.path:
        sys.path.append(path)

