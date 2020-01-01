'''
Definitions on __init__.py
'''
import logging
import os
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class SingleLevelFilter(logging.Filter):
    '''
    Class for log level filtering
    '''
    def __init__(self, passlevel, reject):
        self.passlevel = passlevel
        self.reject = reject

    def filter(self, record):
        if self.reject:
            return (record.levelno != self.passlevel)
        else:
            return (record.levelno == self.passlevel)


def get_logger_instance(name):
    '''
    Method to create instance with custom options on logging
    '''
    path = datetime.now().strftime('%Y-%m-%d.log')
    WO_FUNCTION_FORMAT = '[%(asctime)s] [%(levelname)-8s] %(message)s (%(filename)s:%(lineno)s))'

    formatter = logging.Formatter(WO_FUNCTION_FORMAT, "%Y-%m-%d %H:%M:%S")

    debug_handler = TimedRotatingFileHandler(
        os.path.join(ROOT_DIR, 'logs', 'debug_' + path),
        when="D",
        interval=24,
        backupCount=5)
    debug_handler.setFormatter(formatter)

    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setLevel(logging.INFO)
    screen_handler.setFormatter(formatter)

    stderr_hdlr = logging.StreamHandler(sys.stderr)
    stderr_hdlr.setFormatter(formatter)

    filter1 = SingleLevelFilter(logging.DEBUG, True)

    info_handler = TimedRotatingFileHandler(
        os.path.join(ROOT_DIR, 'logs', 'info_' + path),
        when="D",
        interval=24,
        backupCount=5)
    info_handler.addFilter(filter1)
    info_handler.setFormatter(formatter)

    PERFORMANCE_LEVELV_NUM = 25
    logging.addLevelName(PERFORMANCE_LEVELV_NUM, "LOAD_TIME")

    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
    logger.addHandler(screen_handler)

    return logger
