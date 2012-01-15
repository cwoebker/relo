#!/usr/bin/env python
# encoding: utf-8

import os

from relo.core.config import *


def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False
