# -*- coding:utf-8 -*-
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
import sys
from cobra.conf.GlobalSettings import *
class ReadFile:
    def __init__(self,appName,masterName):
        self.conf = SparkConf().setAppName(appName).setMaster(masterName)
        self.sc = SparkContext(conf=self.conf)

    def readFileForDataFrame(self,path):
        # reload(sys)
        # sys.setdefaultencoding("utf8")
        textFile = self.sc.textFile(path)
        length = textFile.map(lambda s: len(s))
        # textRdd.map(lambda s: len(s)).reduce(lambda a, b: a + b)
        # textFile.collect()
        print length
        # print "textRdd:",textRdd
#######################################################################################################################################
# readFile = ReadFile(appName="spark",masterName="local")
# readFile.readFileForDataFrame(path=HDFS_CONFIG["fs_url"]+"/spark/huouse_migrate/fangtianxia_beijing")
#######################################################################################################################################