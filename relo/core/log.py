#!/usr/bin/env python
# encoding: utf-8

import sys

"""import logging, logging.config



BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

def format_color_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAl': YELLOW,
    'ERROR': RED,
    'EXCEPTION': RED,
}

class reloFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color
    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

LOG_FILENAME = "relo.log"
FILE_FORMAT = "[%(asctime)s] - [%(name)s] - [%(levelname)s] :: %(message)s"
COLOR_FILE_FORMAT = format_color_message(FILE_FORMAT, use_color=False)
CONSOLE_FORMAT = "[%(levelname)s] :: %(message)s"
COLOR_CONSOLE_FORMAT = format_color_message(CONSOLE_FORMAT)

def setup_log(name, info, debug, filelog):
    #creating logging instances
    reloLog = logging.getLogger(__name__)

    if filelog:
        fh = logging.FileHandler(LOG_FILENAME)
        fh.setLevel(logging.DEBUG)
        fileFormatter = reloFormatter(COLOR_FILE_FORMAT, use_color=False)
        fh.setFormatter(fileFormatter)
        reloLog.addHandler(fh)

    ch = logging.StreamHandler()
    if info:
        ch.setLevel(logging.INFO)
    elif debug:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.WARNING)
    cmdFormatter = reloFormatter(COLOR_CONSOLE_FORMAT)
    ch.setFormatter(cmdFormatter)
    reloLog.addHandler(ch)"""


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

    ENDC = '\033[0m'

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
    def debug(self, msg):
        self._stdout(Color.debug("DEBUG: %s\n" % msg))

    def head(self, msg):
        self._stdout(Color.blueArrow('=> ') + Color.head("%s\n") % msg)

    def log(self, msg):
        self._stdout("%s\n" % msg)

    def info(self, msg):
        self._stdout(Color.info("INFO: ") + "%s\n" % msg)

    def warning(self, msg):
        self._stdout(Color.warning("WARNING: %s\n" % msg))

    def error(self, msg):
        self._stderr(Color.error("ERROR: ") + "%s\n" % msg)

    def critical(self, msg):
        self._stderr(Color.critical("CRITICAL: %s\n" % msg))

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