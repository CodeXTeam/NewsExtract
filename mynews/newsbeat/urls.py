from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from newsbeat import views

router = DefaultRouter()
router.register(r'taskresults', views.TaskResultViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^list/$', views.NewsListView.as_view(), name='news-list'),
    url(
        r"^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/$",
        views.news_detail, name='news-detail'),
]


'''
app_name = 'newsbeat'
urlpatterns = [
    url(r'^$', views.NewsListView.as_view(), name='newsbeat_list'),
    url(r'^list/$', views.TaskResultList.as_view(), name='taskresult-list'),
    url(r'^list/<int:pk>/',views.TaskResultDetail.as_view(), name='taskresult-detail'),
]
'''