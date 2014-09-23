#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from django import forms

from .models import User


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'patronymic', 'phone', 'company_name', 'city', 'call_from', 'call_to' )

