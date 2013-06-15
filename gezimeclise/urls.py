from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'gezimeclise.views.home', name='home'),
    # url(r'^gezimeclise/', include('gezimeclise.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
