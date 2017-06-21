"""
Simple logging utility for console logs-like output formatting
"""

import logging

def get_logger(logger_name: str, loglevel=logging.INFO, **kwargs) -> logging.Logger:
    """
    Create a logger with specified name and loglevel    
    """
    logger = logging.getLogger(logger_name)

    logger.addFilter(LogFormatter())
    syslog = logging.StreamHandler()
    formatter = logging.Formatter('%(level_label)s %(message)s')
    syslog.setFormatter(formatter)
    logger.addHandler(syslog)
    logger.setLevel(loglevel)    
    return logger

class LogFormatter(logging.Filter):
    def filter(self, record):                
        labels_dict = {
            logging.DEBUG: '[.]',
            logging.INFO: '[+]',
            logging.WARN: '[!]',
            logging.ERROR: '[-]',
            logging.FATAL:    '[ FATAL! ]',
            logging.CRITICAL: '[CRITICAL]'
        }
        record.level_label = labels_dict[record.levelno]

        return True