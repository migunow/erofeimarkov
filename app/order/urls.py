from django.conf.urls import patterns, url

from .views import OrderView, QuickOrder, CallMeBack

urlpatterns = patterns(
    'order.views',
    url(r'^order/$', OrderView.as_view(), name='order_checkout'),
    url(r'^quick_order/$', QuickOrder.as_view(), name='quick_order'),
    url(r'^callme_back/$', CallMeBack.as_view(), name='callme_back'),
    # url(r'$', 'order.views.order_checkout', name='order_checkout'),
);
