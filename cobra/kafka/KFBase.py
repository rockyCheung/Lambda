# coding:utf-8

from pykafka.client import KafkaClient
from cobra.conf.GlobalSettings import *
import logging as log
log.basicConfig(level=log.INFO)
class Base:

    def __init__(self):
        self.client = KafkaClient(KAFKA_CONFIG["hosts"])

    ############################################################################################
    # 获取topic，如果topicName=None返回所有topic字典，如果不为空则返回单条topic
    ############################################################################################
    def getTopics(self,topicName):
        if topicName is None:
            return self.client.topics
        else:
            return self.client.topics[topicName]