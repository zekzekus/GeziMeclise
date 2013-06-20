from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
<<<<<<< HEAD
=======
from gezimeclise.profiles import urls as gezimeclise_url
from gezimeclise.blog import urls as blog_url
>>>>>>> 2a1adf9fe83fbd2c270b58c452c8ef1471ed4b5c
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="landing_page"),
    url(r'^admin/', include(admin.site.urls)),
<<<<<<< HEAD
    url(r'^profiles/', include('gezimeclise.profiles.urls')),
=======
    url(r'^blog/',include(blog_url)),
    url(r'^profiles/', include(gezimeclise_url)),
>>>>>>> 2a1adf9fe83fbd2c270b58c452c8ef1471ed4b5c
    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^accounts/', include('django_facebook.auth_urls'))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
