from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from newsbeat import views

router = DefaultRouter()
router.register(r'taskresults', views.TaskResultViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^list/$', views.list, name='result-list'),
]


'''
app_name = 'newsbeat'
urlpatterns = [
    url(r'^$', views.NewsListView.as_view(), name='newsbeat_list'),
    url(r'^list/$', views.TaskResultList.as_view(), name='taskresult-list'),
    url(r'^list/<int:pk>/',views.TaskResultDetail.as_view(), name='taskresult-detail'),
]
'''