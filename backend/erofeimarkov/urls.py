from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^authentication/', include('authentication.urls', namespace='authentication')),
    url(r'^catalog/', include('catalog.urls', namespace='catalog')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^order/', include('order.urls', namespace='order')),
    url(r'', include('pages.urls', namespace='pages')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (
            r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        )
    )

urlpatterns += patterns(
    '',
    url(r'^$', RedirectView.as_view(url=reverse_lazy('catalog:catalog'), permanent=False)),
)

