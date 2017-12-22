# -*- coding:utf-8 -*-
import logging
import logging.handlers
from cobra.conf.GlobalSettings import *
"""
# logger类
"""
class Logger:
    def __init__(self):
        self.handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
        self.fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        self.formatter = logging.Formatter(self.fmt)  # 实例化formatter
        self.handler.setFormatter(self.formatter)  # 为handler添加formatter

    def getLogger(self,loggerName):
        logger = logging.getLogger(loggerName)
        logger.addHandler(self.handler)
        logger.setLevel(self.debugLevel(LOGGER_LEVEL))
        return logger

    def debugLevel(self,level):
        if level=="DEBUG":
            return logging.DEBUG
        else:
            return logging.INFO