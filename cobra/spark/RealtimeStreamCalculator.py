# -*- coding:utf-8 -*-
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
import time
from cobra.conf.GlobalSettings import *
from cobra.spark.SparkConfigSingleton import *
from pyspark.sql import Row
class RealtimeStreamCalculator:
    def __init__(self,appName,masterName):
        self.config = SparkConfigSingleton(appName,masterName)
        self.sc = SparkContext(conf=self.config.getSparkConf())
        self.ssc = StreamingContext(sparkContext=self.sc,batchDuration=BATH_DURATION)

    def readFileForRDD(self,path):
        textRdd = self.sc.textFile(path,use_unicode=False)
        # parts = textRdd.map(lambda l: l.split(","))
        # length = textRdd.map(lambda s: len(s))
        # textRdd.map(lambda s: len(s)).reduce(lambda a, b: a + b)
        # textFile.collect()
        # print length
        # print textRdd.collect()
        # print str(parts).replace('u\'','\'').decode("unicode-escape")
        return textRdd

    def readStream(self,path):
        dStream = self.ssc.textFileStream(directory=path)
        transFormerString = dStream.flatMap(lambda s:s.split(","))
        print transFormerString
        print "transFormerString:",dStream.pprint(num=10)
        # wordCounts = transFormerString.reduceByKey()
        checkTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # self.process(transFormerString)
        # print "@",transFormerString
        self.ssc.start()
        self.ssc.awaitTermination()

    def getSparkSessionInstance(sparkConf):
        if ("sparkSessionSingletonInstance" not in globals()):
            globals()["sparkSessionSingletonInstance"] = SparkSession \
                .builder \
                .config(conf=sparkConf) \
                .getOrCreate()
        return globals()["sparkSessionSingletonInstance"]

    def process(rdd):
        # print("========= %s =========" % str(time))
        try:
            # Get the singleton instance of SparkSession
            spark = RealtimeStreamCalculator.getSparkSessionInstance(rdd.context.getConf())

            # Convert RDD[String] to RDD[Row] to DataFrame
            rowRdd = rdd.map(lambda w: Row(word=w))
            wordsDataFrame = spark.createDataFrame(rowRdd)

            # Creates a temporary view using the DataFrame
            wordsDataFrame.createOrReplaceTempView("words")

            # Do word count on table using SQL and print it
            wordCountsDataFrame = spark.sql("select word, count(*) as total from words group by word")
            wordCountsDataFrame.show()
        except:
            pass
