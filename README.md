# Lambda
Cobra是一个大数据实时处理，计算的项目。

主要的功能模块：
   1、批量数据迁移
   2、实时数据处理、运算
   目前支持的迁移操作是从mongo迁移到HDFS。
   
项目结构：
    cobra.
      conf.
        GlobalSettings.py
      db.
        MongodbClient.py
      hdfs.
        HDFSClient.py
      kafka.
        Consumer.py
        KFBase.py
        Producer.py
      log.
        Logger.py
      migrate.
        DataMigrate.py
      spark.
        CheckPointParquet.py
        RealtimeStreamCalculator.py
        SparkConfigSingleton.py
    main.py
    setup.py
    requirement.rst	
    writePoint.parquet
    Cobra.egg-info
    dist
    
用到主要技术：
    项目中用到了mongodb、hdfs、sparkSQL
    
工作原理：
    借助mongo客户端批量读取已经处理过的数据，然后通过hdfs客户端自动根据collection名称创建文件，并将数据写入hdfs，同时生成读取check点，记入parquet。
    Apache Parquet是Hadoop生态圈中一种新型列式存储格式，它可以兼容Hadoop生态圈中大多数计算框架(Hadoop、Spark等)，被多种查询引擎支持（Hive、Impala、Drill等），并且它是语言和平台无关的。
 
 使用说明：
    GlobalSettings为全局属性定义类，包括Mongo、HDFS、KAFKA、Zookeeper等相关的配置
    from cobra.conf.GlobalSettings import *
    #获取zookeeper 集群地址
    para = KAFKA_ZOO_CONFIG['hosts']
    Logger为日志类
    from cobra.log.Logger import Logger
    logger = Logger().getLogger('DataMigrate')
    #%s为格式化占位符
    logger.info( "#"+"workPath: %s,collectionNames: %s,append str: %s",workPath,name,tempStr)
    MongodbClient为Mongo客户端
    client = MongodbClient('192.168.1.178',27017)
    #house_orignal数据库名称
    db = client.getConnection('house_orignal')
    #获取数据库中所有collection名称
    collectionNames  = db.collection_names()
    #获取名称为ABC_sale的collection的数据集
    dataSet = db.ABC_sale
    #获取游标
    cursor1 = dataSet.find().skip(1)
    #设置游标的超时时间为永久
    cursor1.add_option(16)
    
    
    
