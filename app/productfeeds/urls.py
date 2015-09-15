#coding: utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^google/$', 'productfeeds.views.googleFeed'),
    url(r'^yamarket/$', 'productfeeds.views.yamarketFeed'),
    url(r'^wikimart/internal/$', 'productfeeds.views.wikimartFeed'),
)
