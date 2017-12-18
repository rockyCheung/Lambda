# -*- coding: UTF-8 -*-

"""
Default  settings. Override these with settings in the module pointed to
by the  environment variable.
"""

####################
# CORE             #
####################
ROOT_PATH = "/data"
DEBUG = False
LOG_FILE = "cobra.log"
#检查点信息写入模式overwrite：覆盖 append：追加
PARQUET_SAVE_MODE = "append"
######################
# MONGODB ip and port#
######################
MONGODB_CONFIG = {
    "ip":"192.168.1.178",
    "port":27017
}
#########################
#HDFS config ip and port#
#########################
HDFS_CONFIG = {
    "hosts":"192.168.1.171:50070",
    "randomize_hosts":True,
    "user_name":"root",
    "timeout":20,
    "max_tries":2,
    "retry_delay":5,
    "fs_url":"hdfs://192.168.1.171:9000"

}
###################################
# schedule start time, 7200 second#
###################################
SCH_INC = 7200
##################################################
# 每执行5次，定时任务重新开始统计次数，定时任务休眠5小时 #
##################################################
EXCUTE_TIMES = 5
SLEEP_TIME = 36000