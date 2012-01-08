#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from relo.core.config import *
from relo.core.exceptions import ShellException
from relo.core.log import logger

def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False