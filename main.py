#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cobra.migrate.DataMigrate import DataMigrate
import sys
import time
from cobra.conf.GlobalSettings import *
import sched
import os
import traceback
from cobra.log.Logger import Logger

try:
    os.mknod(LOG_STD_FILE)
except Exception:
    print "creat file failed.",Exception

log_file = open(LOG_STD_FILE, "a")
sys.stdout = log_file
logger = Logger().getLogger('main')
# 初始化sched模块的scheduler类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)
#########################################################################################
# inc 默认定时60秒
#
#########################################################################################
def main(dbName,savePath, inc=60):
    # enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    # 给该触发函数的参数（tuple形式）
    schedule.enter(inc, 0, excuteMigrateTask, (dbName,savePath))
    schedule.run()
##########################################################################################
# dbName is mongodb database name
# path is data save path in hdfs
##########################################################################################
def excuteMigrateTask(dbName,savePath):
    dataMig = DataMigrate()
    dataMig.migrate(dbName=dbName,path=savePath)

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding("utf8")
    startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logger.info( "excute main ,the default encoding is %s start time %s",sys.getdefaultencoding(),startTime)
    try:
        times = 0
        while True:
            taskStartTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logger.info( "this task start time:"+ taskStartTime)
            if times==0:
                main(dbName=MONGO_DBNAME, savePath=HDFS_PATH, inc=0)
            elif times==EXCUTE_TIMES:
                time.sleep(SLEEP_TIME)
                times = 0
            else:
                main(dbName=MONGO_DBNAME, savePath=HDFS_PATH, inc=SCH_INC)
            endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logger.info( "this task end time: %s  times: %s",endTime,times)
            times +=1
    except Exception,e:
        traceback.print_exc(file=open(ERROR_LOG,'w+'))
    finally:
        log_file.close()
        timestemp = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
        os.rename(LOG_STD_FILE,LOG_STD_FILE+"."+timestemp)