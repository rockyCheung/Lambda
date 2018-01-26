# -*- coding:utf-8 -*-
from cobra.kafka.Consumer import Consumer
import bson
from cobra.db.MongodbClient import  MongodbClient
from cobra.conf.GlobalSettings import *

######################################################
con = Consumer()
mongoClient = MongodbClient(ip=MONGODB_CONFIG["ip"], port=MONGODB_CONFIG["port"])

simple = con.getSimpleConsumer(topicName='topic_test_1',group=None)
for message in simple:
    if message is not None:
        msgValue = str(message.value)
        print message.offset
        # msg = ast.literal_eval(message.value)
        print '@@@@@@',msgValue.startswith('{',0)
        if msgValue.startswith('{',0) and msgValue.endswith('}'):
            msg = {}
            try:
                msg = eval(msgValue)
            except Exception:
                print 'this msg contain can not analysis Object'
            if len(msg) > 0:
                print 'bson:',bson.ObjectId(msg['_id'])
                mongoClient.update(dataBaseName='lhhs', collectionName='article_text', updateFor={'_id': bson.ObjectId(msg['_id'])},
                                   setValue={'$set': {'status': 4}})
        else:
            print msgValue
        # msg = eval(message.value)

print '######################################################'
# balance = con.getBalanceConsumer(topicName='topic_test_1',group='5')
# for message in balance:
#     if message is not None:
#         print message.offset, message.value