#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

# Dynamically calculate the version based on playlister VERSION.

setup(
    name = "adama",
    version = "0.1",
    url = 'http://bitbucket.org/agrausem/commander',
    download_url = 'http://bitbucket.org/agrausem/commander/files/',
    author = 'Arnaud Grausem',
    author_email = 'arnaud.grausem@gmail.com',
    description = 'A light library to create command line python script for an application',
    packages = ['adama', 'adama.orders'],
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
