from __future__ import absolute_import, unicode_literals
from newsbeat.newsmain import run
from celery import shared_task, task



@shared_task
def task_news():
    print('running task_news.')

    result =  run()
    return result
   