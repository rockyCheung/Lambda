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