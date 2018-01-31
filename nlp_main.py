#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cobra.celery.Task import *
from cobra.log.Logger import Logger

logger = Logger().getLogger('nlp_main')

if __name__=="__main__":
    print '##################################################################################'
    print '# 启动task articlesTransformTask 输入：1 ' \
          'sendArticleToProducerTask 输入：2 ' \
          'receiveArticlesFromConsumerTask 输入：3'
    print '##################################################################################'
    str = raw_input("请输入启动服务名称：")
    if str == 1:
        print 'start excute articlesTransformTask'
        articlesTransformTask.delay()
        print 'start excute articlesTransformTask end!'
    elif str == 2:
        sendArticleToProducerTask.delay()
    elif str == 3:
        receiveArticlesFromConsumerTask.delay()
    else:
        print 'start excute '
        add.delay()
        print 'start excute end!'

