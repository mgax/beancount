#!/usr/bin/env python
"""
Install script for beancount.
"""

__author__ = "Martin Blais <blais@furius.ca>"

import os
from os.path import join, isfile
from setuptools import setup


# Install all scripts under bin.
scripts = [join('bin', x) for x in ('bean-web',
                                    'bean-trial',
                                    'bean-suck',
                                    'bean-convert-ofx',
                                    'bean-convert-paypal-csv',
                                    'bean-convert-rbc-activity',
                                    )]

def read_version():
    try:
        return open('VERSION', 'r').readline().strip()
    except IOError, e:
        raise SystemExit(
            "Error: you must run setup from the root directory (%s)" % str(e))

setup(name="beancount",
      version=read_version(),
      description=\
      "Command-line Double-Entry Accounting",
      long_description="""
A double-entry accounting system that uses a simple text file format
as input. A few Python scripts are used to parse the contents of the
file, for example, to serve the contents as a locally running web
server. Scripts are provided to convert from OFX files into Ledger
input format, and other formats (easily extensible). 
""",
      license="GPL",
      author="Martin Blais",
      author_email="blais@furius.ca",
      url="http://furius.ca/beancount",
      package_dir = {'': 'lib/python'},
      packages = ['beancount',
                  'beancount.web',
                  'beancount.fallback',
                  'beancount.fallback.elementtree',
                  ],
      scripts=scripts
     )


