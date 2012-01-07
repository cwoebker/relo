#!/usr/bin/env python
# encoding: utf-8

import sys

LEVEL = {
    'NORMAL': 0,
    'INFO': 1,
    'DEBUG': 2,
    'CRITICAl': 0,
    'ERROR': 0,
    'EXCEPTION': 0,
}

class Color(object):
    ESCAPE = '\033[%sm'
    BOLD = '1;%s'
    UNDERLINE = '4;%s'

    BLUE_ARROW = ESCAPE % (BOLD % '34') # Blue Bold

    DEBUG = ESCAPE % (BOLD % '35') # Magenta Bold
    HEAD = ESCAPE % (BOLD % '1') # Bold White (Standard Color)
    INFO = ESCAPE % '32' # Green Normal
    WARNING = ESCAPE % '33' # Yellow Normal
    ERROR = ESCAPE % '31' # Red Normal
    CRITICAL = ESCAPE % (UNDERLINE % '31') # Red Underline

    # SPECIAL
    ITEM = ESCAPE % (BOLD % '37') # Black Bold/Bright
    SUBITEM = ESCAPE % '37' # White Normal

    ENDC = ESCAPE % '0'

    @classmethod
    def _deco(cls, msg, color):
        return '%s%s%s' % (color, msg, cls.ENDC)
    @classmethod
    def blueArrow(cls, msg):
        return cls._deco(msg, cls.BLUE_ARROW)
    @classmethod
    def head(cls, msg):
        return cls._deco(msg, cls.HEAD)
    @classmethod
    def debug(cls, msg):
        return cls._deco(msg, cls.DEBUG)
    @classmethod
    def info(cls, msg):
        return cls._deco(msg, cls.INFO)
    @classmethod
    def warning(cls, msg):
        return cls_deco(msg, cls.WARNING)
    @classmethod
    def error(cls, msg):
        return cls._deco(msg, cls.ERROR)
    @classmethod
    def critical(cls, msg):
        return cls._deco(msg, cls.CRITICAL)

    @classmethod
    def item(cls, msg):
        return cls._deco(msg, cls.ITEM)
    @classmethod
    def subitem(cls, msg):
        return cls._deco(msg, cls.SUBITEM)

class Logger(object):
    def __init__(self):
        self.level = 0
    def debug(self, msg):
        if self.level >= LEVEL['DEBUG']:
            self._stdout(Color.debug("DEBUG: ") + "%s\n" % msg)
    def head(self, msg):
        self._stdout(Color.blueArrow('=> ') + Color.head("%s\n") % msg)

    def log(self, msg):
        self._stdout("%s\n" % msg)

    def info(self, msg):
        if self.level >= LEVEL['INFO']:
            self._stdout(Color.info("INFO: ") + "%s\n" % msg)

    def warning(self, msg):
        self._stdout(Color.warning("WARNING: ") + "%s\n" % msg)

    def error(self, msg):
        self._stderr(Color.error("ERROR: ") + "%s\n" % msg)

    def critical(self, msg):
        self._stderr(Color.critical("CRITICAL: ") + "%s\n" % msg)

    def item(self, msg):
        self._stdout(Color.item(" - %s\n" % msg))
    def subitem(self, msg):
        self._stdout(Color.subitem("   @ %s\n" % msg))

    def _stdout(self, msg):
        sys.stdout.write(msg)
        sys.stdout.flush()
    def _stderr(self, msg):
        sys.stderr.write(msg)
        sys.stderr.flush()

logger = Logger()