# -*- coding: utf-8 -*- 
from django.conf.urls.defaults import patterns, include, url

from greenmine.views.api import ApiLogin, UserListApiView

urlpatterns = patterns('',
    url(r'^login$', ApiLogin.as_view(), name='login'),
    url(r'^user/list/$', UserListApiView.as_view(), name='user-list'),
    #url(r'^project/create$', ApiCreateProject.as_view(), name='api-progect-create'),
)

