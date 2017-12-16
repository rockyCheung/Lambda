#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cobra.migrate.DataMigrate import DataMigrate
import sys
import time
from cobra.conf.GlobalSettings import *
import sched
import os

log_file = open(LOG_FILE, "a")
sys.stdout = log_file
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
    print "excute main", "the default encoding is ", sys.getdefaultencoding()," start time ",startTime
    try:
        # while True:
        main(dbName="house_orignal", savePath="huouse_migrate",inc=SCH_INC)
        endTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print "the task excute end!","end time ",endTime
    finally:
        log_file.close()
        os.rename(LOG_FILE,LOG_FILE+"."+startTime)