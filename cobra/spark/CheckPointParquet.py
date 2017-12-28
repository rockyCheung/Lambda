# -*- coding:utf-8 -*-

from pyspark.sql import SparkSession
from cobra.conf.GlobalSettings import *

class CheckPointParquet:
    def __init__(self,appName,masterName):
        # self.config = SparkConfigSingleton(appName, masterName)
        self.spark  = SparkSession.builder.appName(appName).config("spark.sql.warehouse.dir", WAREHOUSE_LOCATION).master(masterName).getOrCreate()
        self.parquetLocation = PARQUET_LOCATION+"/writePoint.parquet"

    def writeCheckParquet(self,checkData,saveMode):
        checkDataFrame = self.spark.createDataFrame(checkData,["dbName","collectionName","lastDataHash","position","time"])
        checkDataFrame.write.save(self.parquetLocation, mode=saveMode)

    def queryCheckParquet(self):
        # df = spark.read.load("examples/src/main/resources/users.parquet")
        parquetFile = self.spark.read.parquet(self.parquetLocation)
        parquetFile.createOrReplaceTempView("writePoint")
        # parquetFile.select
        return self.spark.sql("select * from writePoint")

    def queryCheckParquetForCondition(self,dbName,collectionName):
        parquetFile = self.spark.read.parquet(self.parquetLocation)
        parquetFile.createOrReplaceTempView("writePoint")
        statement = "select * from writePoint where dbName='"+dbName+"' and collectionName='"+collectionName+"'"
        print "the query SQL" \
              "is ",statement
        return self.spark.sql(statement)

    def queryCheckParquetMaxPos(self, dbName, collectionName):
        parquetFile = self.spark.read.parquet(self.parquetLocation)
        parquetFile.createOrReplaceTempView("writePoint")
        statement = "select MAX(position) as position from writePoint where dbName='" + dbName + "' and collectionName='" + collectionName + "'"
        print "the query SQL" \
                  "is ", statement
        return self.spark.sql(statement)
