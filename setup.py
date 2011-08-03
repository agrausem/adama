#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages

path = '{0}/src'.format(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)

module = __import__("adama")
version = module.get_version()
project = module.__name__

setup(
    name = project,
    version = version,
    url = 'http://bitbucket.org/agrausem/{0}'.format(project),
    download_url = 'http://bitbucket.org/agrausem/{0}/files/'.format(project),
    author = 'Arnaud Grausem',
    author_email = 'arnaud.grausem@gmail.com',
    description = 'A light library to create command line python script for an application',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    package_data = {
            'adama': [
                'templates/*.template'
            ]
    },
    scripts = ['bin/adama'],
    classifiers = ['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Developers',
                   'Intended Audience :: End User/Desktop'
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Librarie'
                   ],
)
