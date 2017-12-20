# -*- coding:utf-8 -*-
import pyhdfs
import time

class HDFSClient:
    # ###########################################################
    # hdfs地址ip:port，randomize_hosts选取DataNode的策略，
    # user_name访问dataNode用户名称，timeout请求dataNode的超时时间
    # max_tries是最大尝试次数
    # retry_delay重试延时
    ##############################################################
    def __init__(self,hosts,randomizeHosts,userName,timeout,maxTries,retryDelay):
        self.hosts = hosts
        self.randomize_hosts = randomizeHosts
        self.user_name = userName
        self.timeout = timeout
        self.max_tries = maxTries
        self.retry_delay = retryDelay
        self.client = pyhdfs.HdfsClient(hosts=self.hosts,
                                        randomize_hosts=self.randomize_hosts,
                                        user_name=self.user_name,
                                        timeout=self.timeout,
                                        max_tries=self.max_tries,
                                        retry_delay=self.retry_delay,
                                        requests_session=None,
                                        requests_kwargs=None)
    ###############################
    # creat dir
    ###############################
    def mkdir(self,dirName):
        if self.client.exists(dirName)==True:
            print "the dirName is exist"
            return self.client.list_status(dirName)
        else:
            print "the dirName is not exist and will be created"
            return self.client.mkdirs(dirName)
    #############################################
    # write data in file,if file not exist ,creat
    ##############################################
    def append(self,path,fileName,data):
        file = ""
        if str(path).endswith("/"):
            # print "the path end with /"
            file = path+ str(fileName).lower()
        else:
            file = path+"/"+str(fileName).lower()
       # print "the file path is ",file," data:",data
        self.client.set_replication(file, replication=1)
        if self.client.exists(file):
            self.client.append(file,data,buffersize=1024)
        else:
            self.client.create(file,data)

    """
    Return a file-like object for reading the given HDFS path.

            :param offset: The starting byte position.
            :type offset: long
            :param length: The number of bytes to be processed.
            :type length: long
            :param buffersize: The size of the buffer used in transferring data.
            :type buffersize: int
            :rtype: file-like object
    """
    def readFile(self,filePath, **kwargs):
        return self.client.open(filePath)

    def getFileList(self,path):
        if self.client.exists(path):
            return  self.client.listdir(path=path)

    def deleteFile(self,filePath):
        return self.client.delete(path=filePath)
############################################################################
# dfsClient = HDFSClient("192.168.1.171:50070",True,"root",20,2,5)
# # dfsClient.mkdir("/spark/house")
# dfsClient.append("/data/huouse_migrate","fangtianxia_beijing"," {'total_price': '1650', 'facility': '简', 'url': 'http://www.abc001.com/displaySale.do?page=1', 'region': '崇文', 'floor': '5/28', 'release time': '2017-11-29', 'telephone_num': '13911387759', 'area': '230', 'decoration_situation': '中档', 'create_time': datetime.datetime(2017, 11, 29, 5, 31, 5, 608000), 'longitude': '116.416913', 'huxing': '三居', 'latitude': '  39.896528', 'house_type': '民宅', 'contact_person': '曹女士', '_id': 'fae820c236177ce36396e475c22e8d78', 'location': '新世界太华公寓B座517'}")
# fs = dfsClient.readFile("/spark/huouse_migrate/abc_ori",buffersize=1024)
# for i in fs:
#     print "#########################################"
#     print i
#     print "#########################################"