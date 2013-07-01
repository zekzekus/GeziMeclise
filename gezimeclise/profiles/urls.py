from django.conf.urls import patterns, url
from gezimeclise.profiles.views import (ProfileListView,
                                        ProfileDetailView,
                                        ProfileUpdateView,
                                        ProfileSupport,
                                        ProfileDelete)

urlpatterns = patterns('',
    url(r'^$', ProfileListView.as_view(), name="profile_list"),
    url(r'^guncelle/$', ProfileUpdateView.as_view(), name="profile_update"),
    url(r'^destek/$', ProfileSupport.as_view(), name="profile_support"),
    url(r'^sil/$', ProfileDelete.as_view(), name="profile_delete"),
    url(r'^(?P<username>[-\w]+)/$', ProfileDetailView.as_view(),
        name="profile_detail"),
)
