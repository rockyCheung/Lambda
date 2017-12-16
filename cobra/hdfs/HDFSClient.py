# -*- coding:utf-8 -*-
import pyhdfs

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
        if self.client.exists(file):
            self.client.append(file,data)
        else:
            self.client.create(file,data)

    def readFile(self,filePath):
        return self.client.open(filePath)

    def getFileList(self,path):
        if self.client.exists(path):
            return  self.client.listdir(path=path)

    def deleteFile(self,filePath):
        return self.client.delete(path=filePath)
############################################################################
# dfsClient = HDFSClient("192.168.1.171:50070",True,"root",20,2,5)
#dfsClient.mkdir("/spark/house")
# dfsClient.append("/spark","abcdata","WWWWWWWWWWWwwwsssssssss11111111111111")
# dfsClient.readFile("/data/huouse_migrate/abc_ori")