# coding:utf-8

from cobra.kafka.KFBase import Base
from cobra.conf.GlobalSettings import *
"""
# kafka consumer
"""
class Consumer(Base):
    ######################################################
    # 获取simple_consumer
    ######################################################
    def getSimpleConsumer(self,topicName,group):
        return self.getTopics(topicName=topicName).get_simple_consumer(consumer_group=group)

    ######################################################
    # 获取balanced_consumer
    ######################################################
    def getBalanceConsumer(self,topicName,group):
        return self.getTopics(topicName=topicName).get_balanced_consumer(consumer_group=group,auto_commit_enable=True,zookeeper_connect=KAFKA_ZOO_CONFIG['hosts'])

######################################################
# con = Consumer()
# start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# print start
# simple = con.getSimpleConsumer(topicName='topic_test_1',group=None)
# for message in simple:
#     if message is not None:
#         print message.offset, message.value
# print '######################################################'
# balance = con.getBalanceConsumer(topicName='topic_test_1',group='5')
# for message in balance:
#     if message is not None:
#         print message.offset, message.value
######################################################