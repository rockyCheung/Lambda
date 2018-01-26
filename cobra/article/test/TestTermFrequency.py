from pyspark.sql import SparkSession
from cobra.db.MongodbClient import  MongodbClient
from cobra.conf.GlobalSettings import *

# logFile = "/Users/zhangpenghong/Documents/workspace10/Lambda/cobra/article/cobra.log"  # Should be some file on your system
spark = SparkSession.builder.appName('pathcurve').master('local[1]').getOrCreate()
# logData = spark.read.text(logFile).cache()
#
# numAs = logData.filter(logData.value.contains('a')).count()
# numBs = logData.filter(logData.value.contains('b')).count()
#
# print("Lines with a: %i, lines with b: %i" % (numAs, numBs))
mongoClient = MongodbClient(ip=MONGODB_CONFIG["ip"], port=MONGODB_CONFIG["port"])

def queryArticleDataFrame(dbName, collectionName):
    db = mongoClient.getConnection(dataBaseName=dbName)
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
        label = 0
        articleTuple = (label, description, title, url, content, type, heading, keywords)
        articleList.append(articleTuple)
    sentenceData = spark.createDataFrame(articleList,
                                              ["label", "description", "title", "url", "content", "type",
                                               "heading", "keywords"])
    return sentenceData
articleTuple = queryArticleDataFrame(dbName='lhhs', collectionName='article_text')
articleTuple.show()
spark.stop()