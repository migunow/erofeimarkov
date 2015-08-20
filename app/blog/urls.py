# -*- coding: utf-8 -*-
from django.conf.urls import *


urlpatterns = patterns('blog.views',
    url(r'^$', "all_posts"),
    url(r'^(?P<page>\d+)/$', "all_posts", name='all_posts'),
);