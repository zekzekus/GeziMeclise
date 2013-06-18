from django.conf.urls import patterns, url
from gezimeclise.profiles.views import (ProfileListView,
                                        ProfileDetailView,
                                        ProfileUpdateView)

urlpatterns = patterns('',
                       url(r'^$', ProfileListView.as_view(),
                           name="profile_list"),
                       url(r'^get/(?P<username>[-\w]+)/$',
                           ProfileDetailView.as_view(),
                           name="profile_detail"),
                       url(r'^update/$',
                           ProfileUpdateView.as_view()))
