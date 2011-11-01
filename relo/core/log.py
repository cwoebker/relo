__name__ = "relo.log"

import logging, logging.config



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
    reloLog.addHandler(ch)
