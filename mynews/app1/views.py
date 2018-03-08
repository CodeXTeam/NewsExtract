from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.
from .tasks import task_number_one
from django.http import HttpResponse
from django_celery_results.models import TaskResult

def home(request):
    return HttpResponse('Home')

class NewsListView(ListView):
    queryset = TaskResult.objects.all()
    context_object_name = 'infos'
    template_name = 'app1/news/list.html'
    pagniate_by = 5
