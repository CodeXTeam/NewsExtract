from django.shortcuts import render

# Create your views here.

'''
class DjangoCeleryResultsTaskresult(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    hidden = models.BooleanField()
    meta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_taskresult'

'''

from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.
from django.http import HttpResponse
from django_celery_results.models import TaskResult
from rest_framework import generics
from newsbeat.serializers import TaskResultSerializer


def home(request):
    return HttpResponse('Home')


class NewsListView(ListView):
    queryset = TaskResult.objects.all()
    context_object_name = 'infos'
    template_name = 'newsbeat/news/list.html'
    pagniate_by = 5



class TaskResultList(generics.ListAPIView):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer


class TaskResultDetail(generics.RetrieveAPIView):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
