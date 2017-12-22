# coding:utf-8


from cobra.kafka.KFBase import Base

"""
# kafka producer
"""

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