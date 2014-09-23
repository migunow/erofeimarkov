#coding: utf-8
from django.conf.urls import patterns, url
from .views import CartView, OrderView

urlpatterns = patterns(
    'cart.views',
    url(r'order/$', OrderView.as_view(), name="order"),
    url(r'add/$', CartView.as_view(), name="add"),
    url(r'delete/(?P<pk>\d+)/$', CartView.as_view(), name="delete"),
)
