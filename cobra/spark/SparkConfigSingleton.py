# -*- coding:utf-8 -*-
from pyspark import SparkConf
"""
# 创建单例，初始化SparkConf
"""
class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance

class SparkConfigSingleton(Singleton):

    def __init__(self,appName,masterName):
        self.conf = SparkConf().setAppName(appName).setMaster(masterName)
    def getSparkConf(self):
        return self.conf