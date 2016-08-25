from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^bugtracker/', include('bugtracker.urls')),
    url(r'^admin/', admin.site.urls),
]
