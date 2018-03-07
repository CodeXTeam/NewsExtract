from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def task_number_two():
    print('running task 2.')
