from django.conf.urls import patterns, url
from gezimeclise.profiles.views import (ProfileListView,
                                        ProfileDetailView,
                                        ProfileUpdateView,
                                        ProfileSupport, FriendsListView)

urlpatterns = patterns('',
    url(r'^friends_list/$', FriendsListView.as_view(), name="friends_list"),
    url(r'^$', ProfileListView.as_view(), name="profile_list"),
    url(r'^(?P<username>[-\w]+)/$', ProfileDetailView.as_view(), name="profile_detail"),
    url(r'^update/$', ProfileUpdateView.as_view()),
    url(r'^support/$', ProfileSupport.as_view(), name="profile_support"),
)
