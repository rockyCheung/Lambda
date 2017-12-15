# -*- coding:utf-8 -*-

from pyspark.sql import SparkSession

class CheckPointParquet:
    def __init__(self,appName,masterName):
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
#由writePoint.json加载初始信息，创建parquet
# df = spark.read.json("../data/writePoint.json")
# df.show()
# dataFrameWriter = df.write.parquet("writePoint.parquet")
#读取writePoint.parquet信息
# time1  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# dataset = spark.createDataFrame([
#     ("aa", "ss","aaaaaa",1,time1),
#     ("bb", "cc","dddddd",2,time1),
#     ("gg", "ff","yyyyyy",2,time1)
# ], ["dbName", "collectionName","lastDataHash","position","time"])
#
# dataset1 = spark.createDataFrame([
#     ("www", "sas","aaaaasa",1,time1),
#     ("wwwq", "csc","ddsdddd",2,time1),
#     ("ads", "fsf","yyysyyy",2,time1)
# ], ["dbName", "collectionName","lastDataHash","position","time"])
# pandasData1 = dataset1.toPandas()
# pandasData.append(pandasData1, ignore_index=True)
# pdate = pd.merge(dataset,dataset1)
# print pdate
# data = spark.createDataFrame(pandasData)
#dataset.join(dataset1)
# pandasData.show()
# data.write.save("writePoint.parquet",mode="overwrite")
#mergedDF = spark.read.option("mergeSchema", "true").parquet("writePoint.parquet")
# mergedDF = spark.read.option("mergeSchema", "true").parquet("writePoint.parquet")
# mergedDF.printSchema()
#dataset1.createTempView("tempView")
#dataset.write.parquet("writePoint.parquet")



# count = spark.sql("select count(*) as count from writePoint")
# writePointConfig = spark.sql("select * from writePoint")
#
# joined = dataset.join(dataset1,dataset.collectionName==dataset1.collectionName,"outer").collect()
# print joined
# print  writePointConfig.count()
# writePointConfig.show()
# for i in writePointConfig:
#     print i.collectionName
# checkTime  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# checkPoint = CheckPointParquet(appName="CheckPointSpark",masterName="local")
# checkData =  [
#     ("test","clotest","checkString","13",checkTime)
# ]
# checkPoint.writeCheckParquet(checkData,"append")dataFF
# checkPoint.queryCheckParquetForCondition(dbName="test",collectionName="clotest").show()
# dataFF = checkPoint.queryCheckParquetMaxPos(dbName="test",collectionName="clotest")
# dataFF.show()
# data = dataFF.collect()
# for name in data:
#     print name.position