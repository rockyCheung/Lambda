# Lambda
Cobra项目主要用来批量处理Mongo中数据，并批量导入HDFS
项目结构：
    包cobra
    主函数main.py
    安装脚本setup.py
    依赖包requirement.rst	
    parquet writePoint.parquet
    
    Cobra.egg-info为打包过程文件
    dist用来存放打包后的文件
    
    项目中用到了mongodb、hdfs、sparkSQL
工作原理：
    借助mongo客户端批量读取已经处理过的数据，然后通过hdfs客户端自动根据collection名称创建文件，并将数据写入hdfs，同时生成读取check点，记入parquet。
    parquet是Apache Parquet是Hadoop生态圈中一种新型列式存储格式，它可以兼容Hadoop生态圈中大多数计算框架(Hadoop、Spark等)，被多种查询引擎支持（Hive、Impala、Drill等），并且它是语言和平台无关的。
    
