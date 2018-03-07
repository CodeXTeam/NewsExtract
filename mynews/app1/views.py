from django.shortcuts import render

# Create your views here.
from .tasks import task_number_one
from django.http import HttpResponse

def home(request):
    return HttpResponse('Home')
    
