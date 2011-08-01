#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.3'

# Dynamically calculate the version based on playlister VERSION.

setup(
    name = "adama",
    version = version,
    url = 'http://bitbucket.org/agrausem/adama',
    download_url = 'http://bitbucket.org/agrausem/adama/files/',
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
