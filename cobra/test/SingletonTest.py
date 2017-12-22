# -*- coding:utf-8 -*-
from pyspark import SparkContext, SparkConf
from cobra.kafka.Producer import Producer
import json
class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class MyClass(Singleton):
    a = 1
    def __init__(self,name):
        self.name = name
        self.conf = SparkConf().setAppName("test").setMaster("local")
    def p(self):
        print self.name


######################################################
# log = Logger().getLogger(loggerName='logtest')
# log.info("sdsdsdsdsddsds")
# sss = lambda LOGGER_LEVEL:(logging.DEBUG if LOGGER_LEVEL=="DEBUG" else logging.INFO)
# print sss
# make a copy of original stdout route
# stdout_backup = sys.stdout
# define the log file that receives your log info
# client = MongodbClient('192.168.1.178',27017)
# # # conn1 = client.getClient()
# db = client.getConnection('house_orignal')
# # collectionNames  = db.collection_names()
# # for name in collectionNames:
# #     print name
# dataSet = db.ABC_sale
# cursor1 = dataSet.find().skip(1)
# cursor1.add_option(16)
# for i in cursor1:
#     print(str(i).replace('u\'','\'').decode("unicode-escape"))
#
# cursor1.close()
############################################################################
# dfsClient = HDFSClient("192.168.1.171:50070",True,"root",20,2,5)
# # dfsClient.mkdir("/spark/house")
# dfsClient.append("/data/huouse_migrate","fangtianxia_beijing"," {'total_price': '1650', 'facility': '简', 'url': 'http://www.abc001.com/displaySale.do?page=1', 'region': '崇文', 'floor': '5/28', 'release time': '2017-11-29', 'telephone_num': '13911387759', 'area': '230', 'decoration_situation': '中档', 'create_time': datetime.datetime(2017, 11, 29, 5, 31, 5, 608000), 'longitude': '116.416913', 'huxing': '三居', 'latitude': '  39.896528', 'house_type': '民宅', 'contact_person': '曹女士', '_id': 'fae820c236177ce36396e475c22e8d78', 'location': '新世界太华公寓B座517'}")
# fs = dfsClient.readFile("/spark/huouse_migrate/abc_ori",buffersize=1024)
# for i in fs:
#     print "#########################################"
#     print i
#     print "#########################################"
#############################################################################
client = Producer()
request = {}
request["name"] = "RockyCheung"
request["sex"] = "man"
request["age"] = 25
request["marry"] = 'Yes'
request["qq"] = '2211'
msg = json.dumps(request)
client.sendMsg(topicName='topic_test_1',message=msg)
print ("{} has been sent successfully~".format(msg))
#############################################################################

#######################################################################################################################################
# readFile = RealtimeStreamCalculator(appName="spark",masterName="local[2]")

# 初始化SparkSession
# # spark = SparkSession \
#         .builder \
#         .appName("RDD_and_DataFrame") \
#         .config("spark.some.config.option", "some-value") \
#         .getOrCreate()
# fsUrl = HDFS_CONFIG["fs_url"]+"/data/judicial_migrate"
# textRdd = readFile.readFileForRDD(path=fsUrl)
# parts = textRdd.map(lambda l: l.split(","))
# readFile.readStream(path=fsUrl)
# employee = parts.map(lambda p: Row(price=p[0], salary=int(p[1])))
# print parts.collect()
# spark.createDataFrame(parts).show()
# dd = RealtimeStreamCalculator("test","local")
#######################################################################################################################################
#
# one = MyClass("rocky")
# two = MyClass("rocky1")
# print one == two,one is two
# one.p()
# two.p()
