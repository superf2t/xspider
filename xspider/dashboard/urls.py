#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^test$', views.test),
    url(r'^debug/(?P<name>\w+)/$', views.debug),
    url(r'^data/$', views.data),
    url(r'^data/(?P<name>\w+)/$', views.result),
    url(r'^time/$', views.test_current_datetime),
    url(r'^api/edit$', views.edit_project),
    url(r'^api/run$', views.run_project),
    url(r'^api/create$', views.create_project),
    url(r'^api/result$', views.result_project),
]