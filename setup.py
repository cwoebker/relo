#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

APP_NAME = 'Relo'
APP_SCRIPT = './relopy'
VERSION = '0.7.0'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Grab requirements.
with open('requirements.txt') as f:
    required = f.readlines()

settings = dict()

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


# Build Helper.
if sys.argv[-1] == 'build':
    try:
        import py2exe
    except ImportError:
        print 'py2exe is required to continue.'
        sys.exit(1)

    sys.argv.append('py2exe')

    settings.update(
        console=[{'script': APP_SCRIPT}],
        zipfile = None,
        options = {
            'py2exe': {
                'compressed': 1,
                'optimize': 0,
                'bundle_files': 1}})

settings.update(
    name = APP_NAME,
    version = VERSION,
    author = "Cecil Woebker",
    author_email = "cwoebker@gmail.com",
    description = ("Recursive Document Content Search in Python"),
    long_description=open('README.rst').read(),
    keywords = "python search document content",
    url = "http://relo.cwoebker.com/",
    packages = ['relo',],
    include_package_data=True,
    install_requires=required,
    license='BSD',
    scripts = ['relopy'],
    classifiers=(
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Text Processing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.3",
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
    ),
    entry_points={
        'console_scripts': [
            'relo = relo:main',
        ],
    }
)

setup(**settings)
