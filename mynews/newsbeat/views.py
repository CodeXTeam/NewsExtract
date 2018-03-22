from django.shortcuts import render, get_object_or_404

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
from rest_framework import generics, viewsets
from newsbeat.serializers import TaskResultSerializer


def home(request):
    return HttpResponse('Home')


class NewsListView(ListView):
    queryset = TaskResult.objects.all()
    context_object_name = 'infos'
    template_name = 'newsbeat/news/list.html'
    pagniate_by = 5

def news_list(request):
    results= TaskResult.objects.all()
    infos = []
    for res in results:
        info = eval(res.result)
        infos.append(info)
    
    return render(request,
                   'newsbeat/news/list.html', context={'infos': infos})


def news_detail(request, year, month, day):
    res = get_object_or_404(
        TaskResult, status='SUCCESS',
        date_done__year=year, date_done__month=month,date_done__day=day)
    
    taskid = res.task_id
    result = eval(res.result)
    date_done = res.date_done
    return render(
        request, 'newsbeat/news/detail.html',
        context={
            'taskid': taskid,
            'result': result,
            'date_done': date_done
        }
    )
    
    

class TaskResultList(generics.ListAPIView):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer


class TaskResultDetail(generics.RetrieveAPIView):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer


class TaskResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer