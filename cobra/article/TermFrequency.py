# -*- coding:utf-8 -*-
from cobra.db.MongodbClient import  MongodbClient
from cobra.conf.GlobalSettings import *
from cobra.log.Logger import Logger
from pyspark.sql import SparkSession
from pyspark.ml.feature import HashingTF, IDF, Tokenizer,StopWordsRemover
from bs4 import BeautifulSoup
from cobra.spark.CheckPointParquet import CheckPointParquet
import pandas as pd
from cobra.nlp.KeywordCuttingMachine import KeywordCuttingMachine
from nltk.probability import FreqDist

class TermFrequency:
    def __init__(self,appName,masterName):
        self.mongoClient = MongodbClient(ip=MONGODB_CONFIG["ip"], port=MONGODB_CONFIG["port"])
        self.logger = Logger().getLogger('TermFrequency')
        self.spark = SparkSession.builder.appName(appName).config("spark.sql.warehouse.dir", WAREHOUSE_LOCATION).master(masterName).getOrCreate()
        self.parquetLocation = PARQUET_LOCATION + "/featureExtract.parquet"
        self.cuttingMachine = KeywordCuttingMachine()
    ######################################################################
    #将文章内容去除网页标签后迁移到article_text,生成关键词
    ######################################################################
    def transformContent(self,dbName,collectionName):
        db = self.mongoClient.getConnection(dataBaseName=dbName)
        dataSet = db[collectionName]
        for i in dataSet.find():
            content = i['content']
            soup = BeautifulSoup(content, 'lxml')
            content = soup.getText()
            i['content'] = self.cuttingMachine.deleSpecialChar(content)
            i['keywords'] = self.cuttingMachine.doCutting(i['content'])
            db.article_text.insert(i)

    def queryArticleDataFrame(self, dbName, collectionName):
        db = self.mongoClient.getConnection(dataBaseName=dbName)
        dataSet = db[collectionName]
        articleList = []
        for i in dataSet.find():
            description = i['description']
            title = i['title']
            url = i['url']
            content = i['content']
            type = i['type']
            heading = i['heading']
            keywords = i['keywords']
            articleTuple = (0, description, title, url, content, type, heading, keywords)
            articleList.append(articleTuple)
        sentenceData = self.spark.createDataFrame(articleList,
                                                  ["label", "description", "title", "url", "content", "type",
                                                   "heading", "keywords"])
        return sentenceData

    ######################################################################
    # 提取文章关键词，计算关键词词频，StopWordsRemover
    ######################################################################
    def featureExtract(self,sentenceDataFrame):
        # tokenizer = Tokenizer(inputCol="description", outputCol="keywords")
        # wordsData = tokenizer.transform(sentenceData)
        remover = StopWordsRemover(inputCol="keywords", outputCol="filtered")
        #设置停用词
        remover.setStopWords(self.cuttingMachine.chineseStopwords())
        #去除文章中的停用词
        removedData = remover.transform(sentenceDataFrame)
        hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=100)
        featurizedData = hashingTF.transform(removedData)
        # alternatively, CountVectorizer can also be used to get term frequency vectors
        idf = IDF(inputCol="rawFeatures", outputCol="features")
        idfModel = idf.fit(featurizedData)
        rescaledData = idfModel.transform(featurizedData)
        resultData = rescaledData.select("label", "description", "title", "url","type",
                                                   "heading","keywords","features")
        # resultData.show()
        resultJson = resultData.toJSON().first()
        # resultData.show()
        print resultJson
        # db.article_feature.save(dict(resultJson))
        resultData.write.save(self.parquetLocation, mode=PARQUET_SAVE_MODE)

    ######################################################################
    # 计算词频并保存都monggo
    ######################################################################
    def caculatTermFrequency(self,sentenceDataFrame):
        keywordsDataFrame = sentenceDataFrame.select("label","keywords")
        keywordsJson = keywordsDataFrame.toJSON().first()
        keywordsJson = eval(keywordsJson)
        # keywords = eval(str(keywordsJson).encode(encoding='utf-8')).keywords
        print keywordsJson['keywords']
        fdist = FreqDist(keywordsJson['keywords'])
        Sum = len(keywordsJson['keywords'])
        for (s, n) in self.cuttingMachine.sortItem(fdist.items()):
            frequencyDict = {}
            # temp = s + str(float(n) / Sum) + "      " + str(n) + '\r\n'
            proportion = str(float(n) / Sum)
            times = str(n)
            self.logger.info('word:%s,proportion:%s,times:%s',s,proportion,times)
            frequencyDict['word'] = s
            frequencyDict['proportion'] = proportion
            frequencyDict['times'] = times
            self.mongoClient.insertItem(dataBaseName='lhhs', collectionName='article_feature', list=frequencyDict)


term = TermFrequency(appName='article',masterName='local[1]')
#term.transformContent(dbName='lhhs',collectionName='article')
articleTuple = term.queryArticleDataFrame(dbName='lhhs', collectionName='article_text')
term.caculatTermFrequency(articleTuple)