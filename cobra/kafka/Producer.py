# coding:utf-8

from pykafka.client import KafkaClient
import logging
import json
from cobra.conf.GlobalSettings import *
from cobra.kafka.Base import Base
logging.basicConfig(level = logging.INFO)

producer_logger = logging.getLogger('producer')
logging.basicConfig(level = logging.DEBUG)

class Producer(Base):

    ############################################################################################
    # 根据指定topic，发送消息
    ############################################################################################
    def sendMsg(self,topicName,message):
        topic = self.getTopics(topicName=topicName)
        with topic.get_sync_producer() as producer:
            producer.produce(message)

#############################################################################
# client = Producer()
# request = {}
# request["name"] = "RockyCheung"
# request["sex"] = "man"
# request["age"] = 25
# request["marry"] = 'Yes'
# msg = json.dumps(request)
# client.sendMsg(topicName='topic_test_1',message=msg)
# producer_logger.info("{} has been sent successfully~".format(msg))
#############################################################################