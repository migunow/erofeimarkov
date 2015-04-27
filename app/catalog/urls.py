#coding: utf-8
from django.conf.urls import patterns, url
from .views import CatalogView, ItemView


urlpatterns = patterns(
    'catalog.views',
    url(r'^$', CatalogView.as_view(), name='catalog'),
    url(r'^(?P<item_id>\d+)/$', ItemView.as_view(), name='item'),
)