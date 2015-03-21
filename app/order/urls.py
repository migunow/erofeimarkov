from django.conf.urls import patterns, url

from .views import OrderView

urlpatterns = patterns(
    'order.views',
    url(r'^order/$', OrderView.as_view(), name='order_checkout'),
    # url(r'$', 'order.views.order_checkout', name='order_checkout'),
);