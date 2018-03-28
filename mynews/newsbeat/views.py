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
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import ListView
# Create your views here.
from django.http import HttpResponse
from django_celery_results.models import TaskResult
from rest_framework import generics, viewsets
from newsbeat.serializers import TaskResultSerializer

# calendar imports
import calendar
from django.utils.timezone import datetime, now, timedelta, utc
from django.http import Http404, HttpResponseRedirect
from django.views.generic import RedirectView
from calendarium.views import MonthView, CalendariumRedirectView


def home(request):
    return HttpResponse('Home')


def news_list(request):
    results = TaskResult.objects.all()
    infos = []
    for res in results:
        info = eval(res.result)
        infos.append(info)

    return render(request,
                  'newsbeat/news/list.html', context={'infos': infos})


class NewsListView(ListView):
    template_name = 'newsbeat/news/list.html'
    paginate_by = 10
    context_object_name = "infos"
    queryset = TaskResult.objects.all().order_by('-date_done')


def news_detail(request, year, month, day):
    try:
        res = get_object_or_404(
            TaskResult, status='SUCCESS',
            date_done__year=year, date_done__month=month, date_done__day=day)
    except TaskResult.DoesNotExist:
        raise Http404("今天没有执行的定时任务哦~")
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


# calendar views
class EventMonthView(MonthView):
    """
    重写calendarium中的monthview，更换为自己的模板
    """
    template_name = 'newsbeat/calendar/event-month.html'

    def dispatch(self, request, *args, **kwargs):
        self.month = int(kwargs.get('month'))
        self.year = int(kwargs.get('year'))
        if self.month not in range(1, 13):
            raise Http404
        if request.method == 'POST':
            if request.POST.get('next'):
                new_date = datetime(self.year, self.month, 1) + timedelta(
                    days=31)
                kwargs.update({'year': new_date.year, 'month': new_date.month})
                return HttpResponseRedirect(
                    reverse('event-month', kwargs=kwargs))
            elif request.POST.get('previous'):
                new_date = datetime(self.year, self.month, 1) - timedelta(
                    days=1)
                kwargs.update({'year': new_date.year, 'month': new_date.month})
                return HttpResponseRedirect(
                    reverse('event-month', kwargs=kwargs))
            elif request.POST.get('today'):
                kwargs.update({'year': now().year, 'month': now().month})
                return HttpResponseRedirect(
                    reverse('event-month', kwargs=kwargs))
        if request.is_ajax():
            self.template_name = 'calendarium/partials/calendar_month.html'
        return super(EventMonthView, self).dispatch(request, *args, **kwargs)


class EventRedirectView(RedirectView):
    """View to redirect to the current month view.
    自动重定向到当前月"""
    permanent = False

    def get_redirect_url(self, **kwargs):
        return reverse('event-month', kwargs={'year': now().year,
                                              'month': now().month})
