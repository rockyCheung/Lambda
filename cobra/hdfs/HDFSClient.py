# -*- coding:utf-8 -*-
import pyhdfs
import time
from cobra.log.Logger import Logger
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
        self.logger = Logger().getLogger('HDFSClient')
    ###############################
    # creat dir
    ###############################
    def mkdir(self,dirName):
        if self.client.exists(dirName)==True:
            self.logger.debug("the dirName is exist")
            return self.client.list_status(dirName)
        else:
            self.logger.debug( "the dirName is not exist and will be created")
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