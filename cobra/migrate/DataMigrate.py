# -*- coding:utf-8 -*-
"""
从mongo迁移到hadoop
"""
from cobra.db.MongodbClient import  MongodbClient
from cobra.conf.GlobalSettings import *
from cobra.hdfs.HDFSClient import HDFSClient
import time
import hashlib
from cobra.spark.CheckPointParquet import CheckPointParquet
import traceback

class DataMigrate:
    # 初始化HDFS客户端、初始化Mongo客户端
    def __init__(self):
        self.hdfsClient = HDFSClient(hosts=HDFS_CONFIG["hosts"],\
                                     randomizeHosts=HDFS_CONFIG["randomize_hosts"],\
                                     userName=HDFS_CONFIG["user_name"],\
                                     timeout=HDFS_CONFIG["timeout"],\
                                     maxTries=HDFS_CONFIG["max_tries"],\
                                     retryDelay=HDFS_CONFIG["retry_delay"])
        self.mongoClient = MongodbClient(ip=MONGODB_CONFIG["ip"],port=MONGODB_CONFIG["port"])
    # 计算md5 hex字符串
    def md5(self,src):
        hashStr = hashlib.md5()
        hashStr.update(src)
        return hashStr.hexdigest()

    # 迁移数据到指定hdfs路径，并创建检查点
    def migrate(self,dbName,path):
        workPath = ROOT_PATH+"/"+path
        self.hdfsClient.mkdir(dirName=workPath)
        db = self.mongoClient.getConnection(dataBaseName=dbName)
        collectionNames = db.collection_names()
        checkPoint = CheckPointParquet(appName="CheckPointSpark", masterName="local")
        for name in collectionNames:
            if name == "error_records":
                continue

            dataSet = db[name]
            checkString = ""
            positionDataFrame = checkPoint.queryCheckParquetMaxPos(dbName=dbName,collectionName=name)
            print "##############################################"
            positionDataFrame.show()
            print "##############################################"
            dataList = positionDataFrame.collect()
            count = 0
            skipPos = 0
            for pos in dataList:
                skipPos = pos.position
            if skipPos is None or str(skipPos).isdigit() != True:
                skipPos = 0
            if skipPos>=dataSet.count():
                skipPos = dataSet.count()-1
            datacursor = dataSet.find().skip(skipPos)
            datacursor.add_option(16)#DBQuery.Option.noTimeout
            print "#############################################################################################################################################"
            print "# dbName:", dbName, " collectionName:", name, " start position:", skipPos," dataSet count:",datacursor.count(with_limit_and_skip=False),"#"
            print "#############################################################################################################################################"
            tempStr = ""
            errorTimes = 0
            for i in datacursor:
                tempStr = str(i).replace('u\'','\'').decode("unicode-escape")
                if tempStr != "":
                    print "#############################################################################################################################################"
                    print "#","workPath:",workPath,"collectionNames:",name," append str:",tempStr
                    print "#############################################################################################################################################"
                    try:
                        self.hdfsClient.append(workPath,name,tempStr)
                    except Exception:
                        traceback.print_exc(file=ERROR_LOG)
                        print Exception, "sleep 60 second"
                        time.sleep(60)
                        errorTimes += 1
                        tempDict = eval(tempStr)
                        tempDict['collectionNames'] = name
                        tempDict['dbName'] = dbName
                        db.error_records.insert(tempDict)
                    count += 1
            datacursor.close()
            checkString = self.md5(tempStr)
                # print(str(i).replace('u\'','\'').decode("unicode-escape"))
            checkTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            ##################################################################
            #数据顺序[(dbName,collectionName,lastDataHash,position,count,checkTime)]
            ###################################################################
            if checkString != "":
                checkPointData = [(dbName,name,checkString,count,checkTime)]
                checkPoint.writeCheckParquet(checkPointData, PARQUET_SAVE_MODE)
            checkPoint.queryCheckParquet().show()
            print "the collection ",name," ,have ",count," lines data"," errorTimes:",errorTimes
###################################################################################################
# tempStr  = "{'name' : 'jim', 'sex' : 'male', 'age': 18}"
# #tempStr = json.loads(tempStr)
# dic = eval(tempStr)
# # print eval(tempStr)
# # js = json.loads(eval(tempStr))
# # tempStr.append({"collectionNames":"n","dbName":"d"})
# dic['collectionNames'] = 'sss'
# dic['dbName'] = 'sssddaa'
# mongoClient = MongodbClient(ip=MONGODB_CONFIG["ip"],port=MONGODB_CONFIG["port"])
# db = mongoClient.getConnection(dataBaseName='house_orignal')
# db.error_records.insert(dic)
# print dic