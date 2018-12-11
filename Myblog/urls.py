from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^index/$', views.index),
    url(r'^list/$', views.list),
    url(r'^blog/(\d+)/$', views.show),
    url(r'^book/(?P<cid>\d+)/$', views.list),
    url(r'^tag/(?P<tid>\d+)/$', views.list),
    url(r'^search/$', views.Search.as_view()),
    url(r'^comment/(\d+)/$', views.CommentArticle.as_view()),


]
