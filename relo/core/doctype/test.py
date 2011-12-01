#!/usr/bin/env python
# encoding: utf-8
import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))
up_dir = os.path.dirname(dirname)
sys.path.append(up_dir)

from relo.core.interfaces import DocType

class TEST(DocType):
    name = "TEST Plugin"