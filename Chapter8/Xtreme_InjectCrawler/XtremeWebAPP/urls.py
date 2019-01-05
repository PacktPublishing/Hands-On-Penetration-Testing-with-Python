from django.conf.urls import patterns, include, url
from xtreme_server.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^/?$', home),
    url(r'^progress/?$', progress),
    url(r'^new/?$', new_scan),
    url(r'^scans/?$', new_scans),
    url(r'^details/?$', get_details),
    url(r'^.*$', disp404)
)
