# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.flatpages.views import render_flatpage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import render_to_response, get_object_or_404

from .models import BlogPage, RECORD_TYPE_BLOG_ENTRY


POSTS_PER_PAGE = 4

def all_posts(self, page=1):
    """
    Show blog pages.
    """
    posts_list = BlogPage.objects.all().filter(page_type=RECORD_TYPE_BLOG_ENTRY).order_by("-pub_date")
    paginator = Paginator(posts_list, POSTS_PER_PAGE)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render_to_response("blog/blog_pages.html", {"posts": posts})


# This view is called from FlatpageFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
# However, we can't just wrap this view; if no matching flatpage exists,
# or a redirect is required for authentication, the 404 needs to be returned
# without any CSRF checks. Therefore, we only
# CSRF protect the internal implementation.
def flatpage(request, url):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if not url.startswith('/'):
        url = '/' + url
    try:
        f = get_object_or_404(BlogPage, url__exact=url)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            f = get_object_or_404(BlogPage, url__exact=url)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    return render_flatpage(request, f)
