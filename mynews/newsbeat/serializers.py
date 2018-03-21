#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-21 14:07:23
# @Author  : cgDeepLearn (cglearningnow@163.com)

from rest_framework import serializers
from django_celery_results.models import TaskResult


class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ('url', 'task_id', 'status', 'content_type', 'result', 'date_done')
