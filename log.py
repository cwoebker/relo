__name__ = "log"

import logging, logging.config

class searchLogger(object):
    def __init__(self, debug):
        LOG_FILENAME = "Relo.log"

        #creating logging instances

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        if debug == 1:
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.INFO)

        fh = logging.FileHandler(LOG_FILENAME)
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter("[%(asctime)s] - [%(levelname)s] :: %(message)s")

        #link logging configuration

        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

        LEVELS = {
            'debug' : logging.DEBUG,
            'info' : logging.INFO,
            'warning' : logging.WARNING,
            'error' : logging.ERROR,
            'critical' : logging.CRITICAL
        }
    def debug(self, msg):
        """sends debug message to logger"""
        self.logger.debug(msg)
    def info(self, msg):
        """sends info message to logger"""
        self.logger.info(msg)
    def warning(self, msg):
        """sends warning message to logger"""
        self.logger.warning(msg)
    def error(self, msg):
        """sends error message to logger"""
        self.logger.error(msg)
    def critical(self, msg):
        """sends critical message to logger"""
        self.logger.critical(msg)
