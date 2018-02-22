# Lambda
Cobra是一个大数据实时处理，计算的项目。
测试数据来源 http://archive.ics.uci.edu/ml/index.php
## 主要的功能模块：
###1、批量数据迁移
###2、实时数据处理、运算
目前支持的迁移操作是从mongo迁移到HDFS。
   
## 项目结构：
>cobra.
>>conf.
>>>GlobalSettings.py
>>db.
>>>MongodbClient.py
>>hdfs.
>>>HDFSClient.py
>>kafka.
>>>Consumer.py
>>>KFBase.py
>>>Producer.py
>>log.
>>>Logger.py
>>migrate.
>>>DataMigrate.py
>spark.
>>>CheckPointParquet.py
>>>RealtimeStreamCalculator.py
>>>SparkConfigSingleton.py
>data
>>>images
>>>featureExtract.parquet
>>>logistic
>>>pipeline
>>>warehouse
>>>writePoint.parquet
>>>stopwords-zh.txt
>>>userdict.txt
>main.py
>setup.py
>requirement.rst
>Cobra.egg-info
>dist
    
## 用到主要技术：

项目中用到了mongodb、hdfs、SparkSQL、SparkStream、SparkML、Celery
    
## 工作原理：

### 1、借助mongo客户端批量读取已经处理过的数据，然后通过hdfs客户端自动根据collection名称创建文件，并将数据写入hdfs，同时生成读取check点，记入parquet。
    
### 2、Apache Parquet是Hadoop生态圈中一种新型列式存储格式，它可以兼容Hadoop生态圈中大多数计算框架(Hadoop、Spark等)，被多种查询引擎支持（Hive、Impala、Drill等），并且它是语言和平台无关的。
 
## 使用说明：
 
### 1、GlobalSettings为全局属性定义类，包括Mongo、HDFS、KAFKA、Zookeeper等相关的配置。

```from cobra.conf.GlobalSettings import *```

`获取zookeeper 集群地址`

```para = KAFKA_ZOO_CONFIG['hosts']```

    
### 2、Logger为日志类

```from cobra.log.Logger import Logger
logger = Logger().getLogger('DataMigrate')```
`#%s为格式化占位符`
```logger.info( "#"+"workPath: %s,collectionNames: %s,append str: %s",workPath,name,tempStr)```
    
### 3、MongodbClient为Mongo客户端
    
```client = MongodbClient('192.168.1.178',27017)
#house_orignal数据库名称
db = client.getConnection('house_orignal')
#获取数据库中所有collection名称
collectionNames  = db.collection_names()
#获取名称为ABC_sale的collection的数据集
dataSet = db.ABC_sale
#获取游标
cursor1 = dataSet.find().skip(1)
#设置游标的超时时间为永久
cursor1.add_option(16)```

### 4、kafka服务提供者和消费者

Producer实现了kafka向消息生产者发送信息的方法sendMsg(topicName,message)
Consumer实现了kafka作为消息消费者订阅消息的方法getSimpleConsumer(topicName,group)、getBalanceConsumer(topicName,group)
        
### 5、celery

```Task.py
CeleryConfig.py```

### 6、人脸识别调用方法

#### face_recognition是什么

`face_recognition基于python开发的人像识别库，其借助blib机器深度学习库实现人脸图像精准识别，识别率高达99.38%。`

```# -*- coding:utf-8 -*-
    import face_recognition
    from cobra.conf.GlobalSettings import *
    from PIL import Image,ImageDraw

    class FaceRecognition(object):
        def __init__(self):
            self.aiface = face_recognition
            self.root = ROOT_PATH

        def loadImage(self,path):
            return self.aiface.load_image_file(self.root+'/'+path)

        def touchFaceImage(self,image):
            face_locations = self.aiface.face_locations(img=image, model="cnn")
            return image, face_locations

        def touchFace(self,path):
            image = self.loadImage(path)
            return self.touchFaceImage(image)

            def landmarksImage(self,image,faceLocations):
                 return image,self.aiface.face_landmarks(face_image=image,face_locations=faceLocations)

        def landmarks(self,path,faceLocations):
            image = self.loadImage(path)
            return self.landmarksImage(image,faceLocations)

        def compareFaces(self,face,unknownFace):
            image = self.loadImage(path=face)
            imageArray, faceLocations = self.touchFaceImage(image=image)
            imageEncoding = self.aiface.face_encodings(image,known_face_locations=faceLocations,num_jitters=1)[0]

            unknown = self.loadImage(path=unknownFace)
            unknownImageArray, unknownFaceLocations = self.touchFaceImage(image=unknown)
            unknownEncoding = self.aiface.face_encodings(unknown,known_face_locations=unknownFaceLocations,num_jitters=1)[0]
            results = self.aiface.compare_faces([imageEncoding], unknownEncoding)
            if results[0] == True:
                print("It's a picture of me!")
            else:
                print("It's not a picture of me!")
            return results[0]

        def showFace(self, image, faceLocations):
            print("I found {} face(s) in this photograph.".format(len(faceLocations)))

            for faceLocation in faceLocations:
            # Print the location of each face in this image
                top, right, bottom, left = faceLocation
                print(
                "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                      right))

            # You can access the actual face itself like this:
                faceImage = image[top:bottom, left:right]
                pilImage = Image.fromarray(faceImage)
                pilImage.show()
        def showFaceLandmarks(self,image,faceLandmarksList):
            print("I found {} face(s) in this photograph.".format(len(faceLandmarksList)))

            for faceLandmarks in faceLandmarksList:

            # Print the location of each facial feature in this image
                facialFeatures = [
                'chin',
                'left_eyebrow',
                'right_eyebrow',
                'nose_bridge',
                'nose_tip',
                'left_eye',
                'right_eye',
                'top_lip',
                'bottom_lip'
                ]

                for facialFeature in facialFeatures:
                print("The {} in this face has the following points: {}".format(facialFeature,
                                                                                 faceLandmarks[facialFeature]))
            # Let's trace out each facial feature in the image with a line!
                pil_image = Image.fromarray(image)
                d = ImageDraw.Draw(pil_image)

                for facialFeature in facialFeatures:
                    d.line(faceLandmarks[facialFeature],fill='red', width=3)

                pil_image.show()```
###### 如何识别仓老师的脸
``` from cobra.aiface. FaceRecognition import FaceRecognition
    aiface = FaceRecognition()
    image,faceLocations = aiface.touchFace('images/canglaoshi.jpeg')
    aiface.showFace(image, faceLocations)```
touchFace返回两个参数，第一个是图片的数字数组，第二个是人脸所在位置，人脸所在位置[top, right, bottom, left]，人脸识别有两种模式，缺省为hot，基本识别模式，识别速度快，但准度低，cnn模式，识别速度慢，精度高，本文中采用都为cnn模式，因为hot模式根本就他娘的无法识别。
![仓老师](http://www.pathcurve.cn/assets/uploads/files/1518572459349-timg.jpeg)
![运行结果](http://www.pathcurve.cn/assets/uploads/files/1518572481295-cangllaoshi_face.png)
###### 如何标识人脸的五官
```   from cobra.aiface. FaceRecognition import FaceRecognition
      aiface = FaceRecognition()
      image,faceLocations = aiface.touchFace('images/chuanpu1.jpg')
      limage,landmarks = aiface.landmarksImage(image,faceLocations)
      aiface.showFaceLandmarks(limage,landmarks)```
![川普](http://www.pathcurve.cn/assets/uploads/files/1518572542642-7a4ed78e28d2aaddf32205c6c38ae33d.jpeg)
![运行结果](http://www.pathcurve.cn/assets/uploads/files/1518572819357-chuanpu_face.png)
川普的脸正标准啊，方方正正的整好做人脸识别～
# 如何对比两张脸是不是同一人
```aiface.compareFaces(face='images/chuanpu1.jpg',unknownFace='images/chuanpu2.jpg')```
如果为同一人返回True

[技术论坛](http://www.pathcurve.cn)


    
    
    
