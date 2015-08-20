# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
#from django.core.urlresolvers import reverse_lazy

from pagedown.widgets import AdminPagedownWidget
#from stickyuploads.widgets import StickyUploadWidget

from .models import BlogPage, BlogImage


class BlogImageAdminForm(forms.ModelForm):
    image = forms.ImageField()

class BlogPageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget)


class BlogImageAdmin(admin.ModelAdmin):
    model = BlogImage
    form = BlogImageAdminForm

    list_display = ('name', 'image_url')

    def image_url(self, obj):
        return '<a href="%s">%s</a>' % (obj.image.url, obj.image.url)
    image_url.allow_tags = True
    image_url.short_description = 'URL'


class BlogPageAdmin(admin.ModelAdmin):
    form = BlogPageAdminForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'pub_date', 'page_type', 'template_name')}),
    )
    list_display = ('url', 'title', 'page_type')
    list_filter = ('sites', 'enable_comments', 'registration_required', 'page_type')


admin.site.register(BlogPage, BlogPageAdmin)
admin.site.register(BlogImage, BlogImageAdmin)