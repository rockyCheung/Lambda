# -*- coding:utf-8 -*-

from pyspark.sql import SparkSession
# from cobra.spark.SparkConfigSingleton import *

class CheckPointParquet:
    def __init__(self,appName,masterName):
        # self.config = SparkConfigSingleton(appName, masterName)
        self.spark  = SparkSession.builder.appName(appName).master(masterName).getOrCreate()
    def writeCheckParquet(self,checkData,saveMode):
        checkDataFrame = self.spark.createDataFrame(checkData,["dbName","collectionName","lastDataHash","position","time"])
        checkDataFrame.write.save("writePoint.parquet", mode=saveMode)
    def queryCheckParquet(self):
        parquetFile = self.spark.read.parquet("writePoint.parquet")
        parquetFile.createOrReplaceTempView("writePoint")
        # parquetFile.select
        return self.spark.sql("select * from writePoint")
    def queryCheckParquetForCondition(self,dbName,collectionName):
        parquetFile = self.spark.read.parquet("writePoint.parquet")
        parquetFile.createOrReplaceTempView("writePoint")
        statement = "select * from writePoint where dbName='"+dbName+"' and collectionName='"+collectionName+"'"
        print "the query SQL" \
              "is ",statement
        return self.spark.sql(statement)

    def queryCheckParquetMaxPos(self, dbName, collectionName):
        parquetFile = self.spark.read.parquet("writePoint.parquet")
        parquetFile.createOrReplaceTempView("writePoint")
        statement = "select MAX(position) as position from writePoint where dbName='" + dbName + "' and collectionName='" + collectionName + "'"
        print "the query SQL" \
                  "is ", statement
        return self.spark.sql(statement)