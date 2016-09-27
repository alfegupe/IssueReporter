# -*- encoding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='bugtracker/')),
    url(r'^bugtracker/', include('bugtracker.urls')),
    url(r'^admin/', admin.site.urls, name='django_admin'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
