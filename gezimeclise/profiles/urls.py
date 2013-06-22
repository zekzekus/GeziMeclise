from django.conf.urls import patterns, url
from gezimeclise.profiles.views import (ProfileListView,
                                        ProfileDetailView,
                                        ProfileUpdateView,
                                        ProfilePostSupport, friends_list_view)

urlpatterns = patterns('',
                       url(r'^$', ProfileListView.as_view(),
                           name="profile_list"),
                       url(r'^get/(?P<username>[-\w]+)/$',
                           ProfileDetailView.as_view(),
                           name="profile_detail"),
                       url(r'^update/$',
                           ProfileUpdateView.as_view()),
                       url(r'^support/$', ProfilePostSupport.as_view()),
                       url(r'^friends/$', friends_list_view, name="friends_list"
                       ))
