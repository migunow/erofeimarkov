#coding: utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^google/$', 'productfeeds.views.googleFeed'),
    url(r'^yamarket/$', 'productfeeds.views.yamarketFeed'),
    url(r'^internal/wikimart/$', 'productfeeds.views.wikimartFeed'),
    url(r'^brilshop/$', 'productfeeds.views.brilshopFeed'),
    url(r'^csv/$', 'productfeeds.views.brilshopFeed'),
)
