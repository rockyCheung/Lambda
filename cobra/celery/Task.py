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
def add():
    s = 1+1
    print '@@@@@@@@',s

