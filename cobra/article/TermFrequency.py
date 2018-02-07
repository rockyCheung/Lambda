# -*- coding:utf-8 -*-
from cobra.db.MongodbClient import  MongodbClient
from cobra.conf.GlobalSettings import *
from cobra.log.Logger import Logger
from pyspark.sql import SparkSession
from pyspark.ml.feature import HashingTF, IDF, Tokenizer,StopWordsRemover
from bs4 import BeautifulSoup
from pyspark.ml import Pipeline,PipelineModel
from pyspark.ml.classification import LogisticRegression
from cobra.nlp.KeywordCuttingMachine import KeywordCuttingMachine
from nltk.probability import FreqDist
from cobra.kafka.Producer import Producer
from cobra.kafka.Consumer import Consumer
import time
import bson

class TermFrequency:
    def __init__(self,appName,masterName):
        self.mongoClient = MongodbClient(ip=MONGODB_CONFIG["ip"], port=MONGODB_CONFIG["port"])
        self.logger = Logger().getLogger('TermFrequency')
        if appName is not None and masterName is not None:
            self.spark = SparkSession.builder.appName(appName).config("spark.sql.warehouse.dir", WAREHOUSE_LOCATION).master(masterName).getOrCreate()
        self.parquetLocation = PARQUET_LOCATION + "/featureExtract.parquet"
        self.cuttingMachine = KeywordCuttingMachine()

    ######################################################################
    # db lhhs  中查询collection article_text文章内容，
    # 支持查询条件、排序
    ######################################################################
    def queryArticles(self,qeury,sort):
        docs = self.mongoClient.query(dataBaseName='lhhs',collectionName='article_text',query=qeury,sort=sort)
        return docs

    ######################################################################
    # 第1步，将文章内容去除网页标签后迁移到article_text,生成关键词
    ######################################################################
    def transformContent(self,dbName,collectionName):
        db = self.mongoClient.getConnection(dataBaseName=dbName)
        collection = db[collectionName]
        for i in collection.find():
            content = i['content']
            soup = BeautifulSoup(content, 'lxml')
            content = soup.getText()
            i['content'] = self.cuttingMachine.deleSpecialChar(content)
            i['keywords'] = self.cuttingMachine.doCutting(i['content'])
            i['status'] = 0 #处理状态，0：未处理 1：待处理 2：处理中 3：处理完成
            i['mtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            db.article_text.insert(i)
            # 删除原collection中的数据
            # collection.delete_one({'_id':i['_id']})

    ######################################################################
    # 将list或dict转化为DataFrame，dict结构
    # {'description':description,'title':title,'url':url,'content':content,'type':type
    # 'heading':heading,'keywords':keywords}
    ######################################################################
    def creatDataFrame(self,articles):
        articleList = []
        tempList = []
        if isinstance(articles,dict):
            tempList.append(articles)

        elif isinstance(articles,list):
            tempList = articles

        else:
            tempList = articles

        for i in tempList:
            description = i['description']
            title = i['title']
            url = i['url']
            content = i['content']
            type = i['type']
            heading = i['heading']
            keywords = i['keywords']
            label = 0
            articleTuple = (label, description, title, url, content, type, heading, keywords)
            articleList.append(articleTuple)
        print articleList
        if len(articleList)>0:
            sentenceData = self.spark.createDataFrame(articleList,
                                                  ["label", "description", "title", "url", "content", "type",
                                                   "heading", "keywords"])
        return sentenceData


    ######################################################################
    # 第2步，从mongo中查询文章内容，并把文章内容按照description、title、url、content
    # type、heading、keywords的顺序创建DataFrame
    ######################################################################
    def queryArticleDataFrame(self,qeury,sort):
        docs = self.queryArticles(qeury,sort)
        return self.creatDataFrame(articles=docs)

    ######################################################################
    # 提取文章关键词，计算关键词词频，StopWordsRemover
    ######################################################################
    def featureExtract(self, trainDataframe,predictionDataframe):
        pipeline = None
        try:
            pipeline = Pipeline.load(ROOT_PATH+'/pipeline')
        except Exception:
            print Exception.message
            self.logger.error(Exception)
        if pipeline is None:
            # tokenizer = Tokenizer(inputCol="keywords", outputCol="words")
            remover = StopWordsRemover(inputCol="keywords", outputCol="filtered")
            # 设置停用词
            remover.setStopWords(self.cuttingMachine.chineseStopwords())
            hashingTF = HashingTF(inputCol=remover.getOutputCol(), outputCol="features")
            idf = IDF(inputCol=hashingTF.getOutputCol(), outputCol="idff")
            # lr = LogisticRegression(maxIter=10, regParam=0.001)
            pipeline = Pipeline(stages=[remover, hashingTF, idf])
        model = pipeline.fit(trainDataframe)
        model.write().overwrite().save(ROOT_PATH+'/pipeline')
        resultDataframe = model.transform(predictionDataframe)
        resultDataframe.show()
        selected = resultDataframe.select("filtered","features", "idff")

        for row in selected.collect():
            filtered,features, idff = row
            self.logger.info("features: %s" , features)
            self.logger.info("idff: %s" ,idff)
            self.logger.info("filtered: %s" ,str(filtered).decode("unicode_escape").encode("utf-8"))


        # resultData.write.save(self.parquetLocation, mode=PARQUET_SAVE_MODE)

    ######################################################################
    # 第3步，计算词频并保存到monggo
    ######################################################################
    def caculatTermFrequency(self,sentenceDataFrame):
        keywordsDataFrame = sentenceDataFrame.select("label","keywords")
        keywordsJson = keywordsDataFrame.toJSON().first()
        keywordsJson = eval(keywordsJson)
        # keywords = eval(str(keywordsJson).encode(encoding='utf-8')).keywords
        # print keywordsJson['keywords']
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

    def stopSpark(self):
        self.spark.stop()

    ######################################################################
    # 发送信息到kafka，并将信息状态设置为等待处理状态
    #
    ######################################################################
    def sendArticleToProducer(self,topic):
        try:
            producer = Producer()
            docs = self.queryArticles(qeury={'status':0}, sort='mtime')
            for i in docs:
                self.logger.info('@send message start')
                id = i['_id']
                i['_id'] = id.__str__()
                i['status'] = 1
                producer.sendMsg(topicName=topic,message=str(i).decode(encoding='unicode_escape').encode(encoding='utf-8'))
                self.logger.info( '@the id:%s',i['_id'])
                self.mongoClient.update(dataBaseName='lhhs',collectionName='article_text',updateFor={'_id':id},setValue={'$set': {'status': 1}})
        except Exception:
            self.logger.info('send message error:%s',Exception.message)
            raise Exception

    ######################################################################
    # 从kafka订阅消息，并将信息进行词频处理，将处理完的结果保存mongo
    #
    ######################################################################
    def receiveArticlesFromConsumer(self,topic):
        consumer = Consumer()
        simple = consumer.getSimpleConsumer(topicName=topic, group=None)
        for message in simple:
            if message is not None:
                msgValue = str(message.value)
                self.logger.info("the message offset:%s",message.offset)
                # msg = ast.literal_eval(message.value)
                if msgValue.startswith('{', 0) and msgValue.endswith('}'):
                    msg = {}
                    try:
                        msg = eval(msgValue)
                    except Exception:
                        self.logger.error('this msg contain can not analysis Object')
                    if len(msg) > 0 and msg['status']==1:
                        self.logger.info('bson:%s', bson.ObjectId(msg['_id']))
                        sentenceDataFrame = self.creatDataFrame(msg)
                        self.caculatTermFrequency(sentenceDataFrame)
                        self.mongoClient.update(dataBaseName='lhhs', collectionName='article_text',\
                                           updateFor={'_id': bson.ObjectId(msg['_id'])},\
                                           setValue={'$set': {'status': 3}})

                else:
                    pass


term = TermFrequency(appName='article',masterName='local[1]')
# term.transformContent(dbName='lhhs',collectionName='article')
try:
    # print 'test'
    # term.transformContent('lhhs', 'article')
    # term.sendArticleToProducer(topic='topic_test_1')
    # docs = term.queryArticles(qeury={'type':'3'},sort='type')
    # for i in docs:
    #     print i
    #articleTuple = term.queryArticleDataFrame(qeury=None,sort=None)
    pipeline = PipelineModel.load(ROOT_PATH + '/pipeline')
    print pipeline
    # articleTuple.show(n=20, truncate=True)
    #term.featureExtract(articleTuple,articleTuple.limit(num=1))
    # term.caculatTermFrequency(articleTuple)
except Exception,e:
    term.stopSpark()
    term.logger.error(e)
    raise e