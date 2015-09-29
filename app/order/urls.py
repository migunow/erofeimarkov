from django.conf.urls import patterns, url

from .views import OrderView, QuickOrder

urlpatterns = patterns(
    'order.views',
    url(r'^order/$', OrderView.as_view(), name='order_checkout'),
    url(r'^quick_order/$', QuickOrder.as_view(), name='quick_order'),
    # url(r'$', 'order.views.order_checkout', name='order_checkout'),
);
