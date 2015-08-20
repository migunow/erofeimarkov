# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.db import models


RECORD_TYPE_PAGE = 0
RECORD_TYPE_BLOG_ENTRY = 1

RECORD_TYPES = (
    (RECORD_TYPE_PAGE, "Произвольная страница"),
    (RECORD_TYPE_BLOG_ENTRY, "Запись блога"),
)


class BlogPage(FlatPage):
    pub_date = models.DateTimeField(blank=True)
    page_type = models.IntegerField(null=False, default=RECORD_TYPE_BLOG_ENTRY,
                                    choices=RECORD_TYPES)

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = datetime.now()

        if self.page_type == RECORD_TYPE_BLOG_ENTRY:
            blog_url = "/blog/page/{slug}/"
            if "/" not in self.url:
                self.url = blog_url.format(slug=self.url)

        super(BlogPage, self).save(*args, **kwargs)

        if not self.sites.all():
            self.sites.add(*[site.id for site in Site.objects.all()])
        super(BlogPage, self).save(*args, **kwargs)

    def next_page(self):
        query = BlogPage.objects.all().filter(page_type=RECORD_TYPE_BLOG_ENTRY)
        query = query.filter(pub_date__gt=self.pub_date).order_by("pub_date")
        try:
            return query[0]
        except IndexError:
            return None

    def previous_page(self):
        query = BlogPage.objects.all().filter(page_type=RECORD_TYPE_BLOG_ENTRY)
        query = query.filter(pub_date__lt=self.pub_date).order_by("-pub_date")
        try:
            return query[0]
        except IndexError:
            return None

    def related_pages(self):
        try:
            query = BlogPage.objects.all().filter(page_type=RECORD_TYPE_BLOG_ENTRY)
            query = query.order_by('?')
            return query[:3]
        except Exception:
            from traceback import print_tb; print_tb()


class BlogImage(models.Model):
    name = models.CharField(max_length=63)
    image = models.ImageField(upload_to="upload/images/")

    def get_image_url(self):
        return self.image.url