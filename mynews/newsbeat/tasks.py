from __future__ import absolute_import, unicode_literals
from celery import shared_task
from news_main import main


@shared_task
def task_news():
    print('running task_news.')
    result =  main()
    return result
   