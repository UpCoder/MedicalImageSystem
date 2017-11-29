from django.conf.urls import url
from front_end import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', views.login),
    url(r'^image/$', views.image),
    url(r'^classification/$', views.classification),
]