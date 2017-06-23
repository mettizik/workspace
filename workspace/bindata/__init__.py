"""
Python package for common utilities to work with binary data
"""
from os.path import abspath, dirname
from sys import path

path.append(abspath(dirname(__file__)))

import tests
