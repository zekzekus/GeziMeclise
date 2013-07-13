from gezimeclise.causes.views import (CausesListView, CauseCreateView,
                                     CauseDetailView, CauseSupportView)
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', CausesListView.as_view(), name="cause_list"),
    url(r'^talep_yarat/$', CauseCreateView.as_view(), name="cause_create"),
    url(r'^destek/$', CauseSupportView.as_view(), name="cause_support"),
    url(r'^(?P<slug>[-\w]+)/$', CauseDetailView.as_view(), name="cause_detail"),

)
