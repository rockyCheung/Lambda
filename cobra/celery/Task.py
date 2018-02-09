# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from cobra.article.TermFrequency import TermFrequency
from cobra.celery.CeleryConfig import app
from cobra.conf.GlobalSettings import *


@app.task
def articlesTransformTask():
    term = TermFrequency(appName=None,masterName=None)
    term.transformContent(dbName='lhhs',collectionName='article')

@app.task
def sendArticleToProducerTask():
    term = TermFrequency(appName='lhhs', masterName='local[2]')
    term.sendArticleToProducer(topic=KAFKA_CONFIG['topic'])
    term.stopSpark()

@app.task
def receiveArticlesFromConsumerTask():
    term = TermFrequency(appName='lhhs', masterName='local[2]')
    term.receiveArticlesFromConsumer(topic=KAFKA_CONFIG['topic'])
    term.stopSpark()

@app.task
def tfIdfTask():
    term = TermFrequency(appName='article', masterName='local[1]')
    articleTuple = term.queryArticleDataFrame(qeury=None, sort=None)
    term.featureExtract(articleTuple, articleTuple.limit(num=1))


@app.task
def lineLogisticTask():
    term = TermFrequency(appName='article', masterName='local[1]')
    articleTuple = term.queryArticleDataFrame(qeury=None, sort=None)
    term.featureExtractLr(articleTuple, articleTuple.limit(num=1))


@app.task
def add(s):
    print 'hello world',s

