from django.conf.urls import url
from . import views

app_name = 'newsbeat'
urlpatterns = [
    url(r'^$', views.NewsListView.as_view(), name='newsbeat_list'),
    url(r'^list/$', views.TaskResultList.as_view(), name='taskresult-list'),
    url(r'^list/<int:pk>/',views.TaskResultDetail.asview(), name='taskresult-detail'),
]