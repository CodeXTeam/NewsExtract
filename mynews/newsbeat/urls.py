from django.conf.urls import url
from . import views

app_name = 'newsbeat'
urlpatterns = [
    url(r'^$', views.NewsListView.as_view(), name='newsbeat_list'),
    url(r'^list/$', views.NewsResultList.as_view(), name='newsresult-list'),
]