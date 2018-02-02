#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cobra.celery.Task import *
from cobra.log.Logger import Logger
'''
#step 1:
    #start celery stak
    #启动角色 worker  执行任务
    #cd Lambda
    $celery -A cobra.celery.Task worker -l info
    #启动角色 beat 将定时任务放到队列中
    $celery -A cobra.celery.Task beat -l info
#step 2:
    #start nlp_main
    $python nlp_main
'''

logger = Logger().getLogger('nlp_main')

if __name__=="__main__":
    print '##################################################################################'
    print '# 启动task articlesTransformTask 输入：1 ' \
          'sendArticleToProducerTask 输入：2 ' \
          'receiveArticlesFromConsumerTask 输入：3'
    print '##################################################################################'
    while True:
        str = raw_input("请输入启动服务名称：")
        if str == '1':
            print 'start excute articlesTransformTask'
            articlesTransformTask.delay()
            print 'start excute articlesTransformTask end!'
        elif str == '2':
            print 'start excute sendArticleToProducerTask'
            sendArticleToProducerTask.delay()
            print 'start excute sendArticleToProducerTask end!'
        elif str == '3':
            print 'start excute receiveArticlesFromConsumerTask'
            receiveArticlesFromConsumerTask.delay()
            print 'start excute receiveArticlesFromConsumerTask end!'
        else:
            print 'start excute '
            for i in range(100):
                print 'thread %d add.start!'%i
                add.delay(i)
            print 'start excute end!'

