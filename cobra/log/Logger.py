# -*- coding:utf-8 -*-
import logging
import logging.handlers
from cobra.conf.GlobalSettings import *

class Logger:
    def __init__(self):
        self.handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
        self.fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        self.formatter = logging.Formatter(self.fmt)  # 实例化formatter
        self.handler.setFormatter(self.formatter)  # 为handler添加formatter
        self.logger = logging.getLogger(LOG_FILE)  # 获取名为tst的logger
        self.logger.addHandler(self.handler)  # 为logger添加handler
        self.logger.setLevel(logging.DEBUG)

# make a copy of original stdout route
# stdout_backup = sys.stdout
# define the log file that receives your log info