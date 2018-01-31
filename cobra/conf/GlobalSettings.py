# -*- coding: UTF-8 -*-
import os
"""
Default  settings. Override these with settings in the module pointed to
by the  environment variable.
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

####################
# CORE             #
####################
ROOT_PATH = BASE_DIR+"/data"
#LOGGER_LEVEL =DEBUG 标识为debug，LOGGER_LEVEL =INFO 标识为info
LOGGER_LEVEL = "DEBUG"
LOG_FILE = BASE_DIR+"/cobra.log"
LOG_STD_FILE = BASE_DIR+"/cobra_std.log"
ERROR_LOG = BASE_DIR+"/cobra_error.log"
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
##################################################
# spark stream 分批时间间隔，单位秒
##################################################
BATH_DURATION = 10

##################################################
# migrate db name and migrate path in hdfs
##################################################
MONGO_DBNAME = "judicial_orignal"
HDFS_PATH = "judicial_migrate"
##################################################
# kafka 集群配置,192.168.100.20:9092,192.168.100.21:9092
##################################################
KAFKA_CONFIG = {
    "hosts":"192.168.100.20:9092,192.168.100.19:9092,192.168.100.21:9092",
    "topic":"topic_test_1"
}

KAFKA_ZOO_CONFIG = {
    "hosts":"192.168.1.175:2181,192.168.1.176:2181,192.168.1.177:2181"
}
##################################################
# warehouse_location
##################################################
WAREHOUSE_LOCATION = ROOT_PATH+'/warehouse'
##################################################
# parquet save path
##################################################
PARQUET_LOCATION = ROOT_PATH
JIEBA_USER_DICT = ROOT_PATH + '/userdict.txt'
JIEBA_STOP_WORDS = ROOT_PATH + '/stopwords-zh.txt'
#mongo broker
BROKER_URL = 'mongodb://192.168.1.178:27017/lhhs'