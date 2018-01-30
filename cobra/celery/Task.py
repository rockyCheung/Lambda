# -*- coding: utf-8 -*-
from celery import Celery
from cobra.conf.GlobalSettings import *
from cobra.article.TermFrequency import TermFrequency
from cobra.conf.Celeryconfig import *
from celery.schedules import crontab

app = Celery('tasks', broker=BROKER_URL)
# app.config_from_object('Celeryconfig')
# Optional configuration, see the application user guide.
app.conf.update(
    enable_utc=True,
    result_expires=3600,
    timezone = 'Asia/Shanghai'
)
# # 每分钟执行一次
# c1 = crontab()
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
        'schedule': cr0
        #'args': ('Hello World', )
    },
}


@app.task
def articlesTransform():
    term = TermFrequency(appName=None,masterName=None)
    term.transformContent(dbName='lhhs',collectionName='article')


