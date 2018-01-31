# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
from cobra.conf.GlobalSettings import *

app = Celery('tasks', broker=BROKER_URL)
# app.config_from_object('Celeryconfig')
# Optional configuration, see the application user guide.
app.conf.update(
    enable_utc=True,
    result_expires=3600,
    timezone = 'Asia/Shanghai',
    accept_content = ['application/json','application/x-python-serialize']
    # accept_content = 'application/x-python-serialize'
)
# # 每分钟执行一次
cr1 = crontab()
#
# # 每天凌晨十二点执行
cr0 = crontab(minute=0, hour=0)
#
# # 每十五分钟执行一次
# crontab(minute='*/15')
#
# # 每周日的每一分钟执行一次
# crontab(minute='*',hour='*', day_of_week='sun')
#
# # 每周三，五的三点，七点和二十二点没十分钟执行一次
# crontab(minute='*/10',hour='3,17,22', day_of_week='thu,fri')

app.conf.beat_schedule = {
    'articles-trasform-perday-12clock': {
        'task': 'Task.articlesTransform',
        'schedule': cr1
        #'args': ('Hello World', )
    },
}
'''
启动角色 worker  执行任务
celery -A cobra.celery.Task worker -l info
启动角色 beat 将定时任务放到队列中
celery -A cobra.celery.Task beat -l info
'''

#启动celery
if __name__ == '__main__':
    app.start()