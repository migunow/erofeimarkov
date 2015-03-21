#coding: utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'phone', 'is_superuser', 'is_staff', 'is_active', 'role' )
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser',)
    search_fields = ('username', )

admin.site.register(User, UserAdmin)
