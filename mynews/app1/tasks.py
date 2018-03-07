from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
import random

@shared_task
def task_number_one():
    print('running task 1.')
    time.sleep(5)
    return random.randint(1, 10)
    
