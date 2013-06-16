from django.conf.urls import patterns, include, url
from django.contrib import admin
from gezimeclise.profiles import urls as gezimecliseurl
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', "home", name="landing_page"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profiles/', include(gezimecliseurl)),
    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^accounts/', include('django_facebook.auth_urls'))
)
