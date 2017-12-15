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
    install_requires=['pyspark>=2.2.0'],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'tip': ['*.msg'],
    },
#    include_package_data=False,
    zip_safe=True,
)