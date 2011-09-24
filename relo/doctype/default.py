#!/usr/bin/env python
# encoding: utf-8

import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))
up_dir = os.path.dirname(dirname)
sys.path.append(up_dir)

from relo.core.interfaces import DocType

import re

class TXT(DocType):
    name = "DEFAULT Plugin"