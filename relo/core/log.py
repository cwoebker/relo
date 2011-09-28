__name__ = "log"

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
    'ERROR': RED
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

class reloLogger(logging.Logger):
    LOG_FILENAME = "relo.log"
    FILE_FORMAT = "[%(asctime)s] - [%(name)s] - [%(levelname)s] :: %(message)s"
    COLOR_FILE_FORMAT = format_color_message(FILE_FORMAT, use_color=False)
    CONSOLE_FORMAT = "[%(levelname)s] :: %(message)s"
    COLOR_CONSOLE_FORMAT = format_color_message(CONSOLE_FORMAT)
    def __init__(self, name, info, debug):
        #creating logging instances
        logging.Logger.__init__(self, name, logging.DEBUG)

        fh = logging.FileHandler(self.LOG_FILENAME)
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        if info:
            ch.setLevel(logging.INFO)
        elif debug:
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.WARNING)

        fileFormatter = reloFormatter(self.COLOR_FILE_FORMAT, use_color=False)
        cmdFormatter = reloFormatter(self.COLOR_CONSOLE_FORMAT)

        #link logging configuration

        fh.setFormatter(fileFormatter)
        ch.setFormatter(cmdFormatter)

        self.addHandler(fh)
        self.addHandler(ch)

        LEVELS = {
            'debug' : logging.DEBUG,
            'info' : logging.INFO,
            'warning' : logging.WARNING,
            'error' : logging.ERROR,
            'critical' : logging.CRITICAL
        }
