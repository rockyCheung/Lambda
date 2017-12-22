# -*- coding:utf-8 -*-
from cobra.kafka.Consumer import Consumer
######################################################
con = Consumer()

# simple = con.getSimpleConsumer(topicName='topic_test_1',group=None)
# for message in simple:
#     if message is not None:
#         print message.offset, message.value
print '######################################################'
balance = con.getBalanceConsumer(topicName='topic_test_1',group='5')
for message in balance:
    if message is not None:
        print message.offset, message.value