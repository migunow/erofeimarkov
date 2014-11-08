#coding: utf-8
from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns(
    'pages.views',
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^contacts/$', TemplateView.as_view(template_name='pages/contacts.html'), name='contacts'),
    url(r'^delivery/$', TemplateView.as_view(template_name='pages/delivery.html'), name='delivery'),
    url(r'^news/$', TemplateView.as_view(template_name='pages/news.html'), name='news'),
    url(r'^offer/$', TemplateView.as_view(template_name='pages/offer.html'), name='offer'),
)
