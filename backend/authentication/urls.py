#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from django.conf.urls import patterns, url
from .views import RegistrationView, LoginView, LogOutView, RestorePasswordView

urlpatterns = patterns(
    'authentication.views',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^restore/$', RestorePasswordView.as_view(), name='restore'),
)