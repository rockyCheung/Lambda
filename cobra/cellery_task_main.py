# -*- coding: utf-8 -*-
from cobra.celery.Task import *
'''
$ celery_task_main -A cobra worker -l info
$ celery_task_main worker --help
#The daemonization scripts uses the celery multi command to start one or more workers in the background
$ celery_task_main multi start w1 -A cobra -l info
#stop the worker
$ celery_task_main multi stop w1 -A cobra -l info
#restart the worker
$ celery  multi restart w1 -A cobra -l info
'''

#启动celery
if __name__ == '__main__':
    app.start()