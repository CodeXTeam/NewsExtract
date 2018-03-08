from django.conf.urls import url
from . import views

app_name = 'app1'
urlpatterns = [
    url(r'^$', views.NewsListView.as_view(), name='news_list')
]