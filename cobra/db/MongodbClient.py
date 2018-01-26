# -*- coding:utf-8 -*-
from pymongo import MongoClient,cursor
from pymongo.collation import Collation

class MongodbClient:

    # 初始化数据库客户端
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = MongoClient(self.ip, self.port)
    ########################################################################################
    # 获取数据库链接，dataBaseName为数据库名称
    ########################################################################################
    def getConnection(self,dataBaseName):
        return self.client[dataBaseName]

    ########################################################################################
    # 插入数据
    ########################################################################################
    def insertItem(self,dataBaseName,collectionName,list):
        db = self.getConnection(dataBaseName=dataBaseName)
        db[collectionName].insert(list)

    ########################################################################################
    # 查询指定db、collection数据集，根据给定查询条件，查询条件为dict，例如{'status':0},sort为排序条件
    # 返回documents
    ########################################################################################
    def query(self,dataBaseName,collectionName,query,sort):
        db = self.getConnection(dataBaseName=dataBaseName)
        collection = db[collectionName]
        if query is not None:
            docs = collection.find(query)
        else:
            docs = collection.find()
        if sort is not None:
            docs = docs.sort(sort)#.collation(Collation(locale='zh-hans'))

        return docs

    ########################################################################################
    # 更新指定数据库、collection中的记录
    # updateSql结构例如：{'first_name': 'jürgen'},{'$set': {'verified': 1}}
    ########################################################################################
    def update(self,dataBaseName,collectionName,updateFor,setValue):
        db = self.getConnection(dataBaseName=dataBaseName)
        collection = db[collectionName]
        result = collection.update_many(updateFor,setValue)
        return result