__name__ = "log"

import logging, logging.config

class Logger(object):
    def __init__(self, debug):
        LOG_FILENAME = "relo.log"

        #creating logging instances

        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        if debug:
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.INFO)

        fh = logging.FileHandler(LOG_FILENAME)
        fh.setLevel(logging.DEBUG)

        fileFormatter = logging.Formatter("[%(asctime)s] - [%(levelname)s] :: %(message)s")
        cmdFormatter = logging.Formatter("[%(levelname)s] :: %(message)s")
        #link logging configuration

        ch.setFormatter(cmdFormatter)
        fh.setFormatter(fileFormatter)

        self.log.addHandler(ch)
        self.log.addHandler(fh)

        LEVELS = {
            'debug' : logging.DEBUG,
            'info' : logging.INFO,
            'warning' : logging.WARNING,
            'error' : logging.ERROR,
            'critical' : logging.CRITICAL
        }
    def debug(self, msg):
        """sends debug message to logger"""
        self.log.debug(msg)
    def info(self, msg):
        """sends info message to logger"""
        self.log.info(msg)
    def warning(self, msg):
        """sends warning message to logger"""
        self.log.warning(msg)
    def error(self, msg):
        """sends error message to logger"""
        self.log.error(msg)
    def critical(self, msg):
        """sends critical message to logger"""
        self.log.critical(msg)
