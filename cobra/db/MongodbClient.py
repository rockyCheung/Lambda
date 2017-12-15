# -*- coding:utf-8 -*-

from pymongo import MongoClient

class MongodbClient:

    # 初始化数据库客户端
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = MongoClient(self.ip, self.port)
    ############################################
    # 获取数据库链接，dataBaseName为数据库名称
    ############################################
    def getConnection(self,dataBaseName):
        return self.client[dataBaseName]

# client = MongodbClient('192.168.1.178',27017)
# # conn1 = client.getClient()
# db = client.getConnection('house_orignal')
# collectionNames  = db.collection_names()
# for name in collectionNames:
#     print name
# dataSet = db.ABC_sale
# for i in dataSet.find():
#     print(str(i).replace('u\'','\'').decode("unicode-escape"))
