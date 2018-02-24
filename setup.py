# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='Cobra',
    version='1.0.0',
    description='The Cobra project is mainly used for batch processing of data in Mongo and batch import of HDFS',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    author='Rocky',
    url='https://github.com/rockyCheung/Cobra.git',
    author_email='274935730@qq.com',
    license='PSF',
    packages=find_packages(),
    install_requires=['pyspark>=2.2.1','face_recognition>=1.2.1','face-recognition-models>=0.3.0','dlib>=19.7',
                      'Pillow>=5.0.0','Click>=6.0','scipy>=0.17.0','numpy>=1.14.1','beautifulsoup4>=4.6.0',
                      'bs4>=0.0.1','nltk>=3.2.5','six>=1.11.0','celery>=4.1.0','amqp>=2.2.2','billiard>=3.5.0.3',
                      'kombu>=4.1.0','pytz>=2018.3','vine>=1.1.4','pymongo>=3.6.0','certifi>=2018.1.18',
                      'chardet>=3.0.4','idna>=2.6','pyhdfs>=0.2.1','requests>=2.18.4','simplejson>=3.13.2',
                      'urllib3>=1.22','kazoo>=2.4.0','pykafka>=2.7.0','tabulate>=0.8.2','jieba>=0.39',
                      'Naked>=0.1.31 pyyaml>=3.12 shellescape>=3.4.1','textblob>=0.15.1','pyttsx3>=2.7','pycrypto>=2.6.1'],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'tip': ['*.msg'],
    },
#    include_package_data=False,
    zip_safe=True,
)