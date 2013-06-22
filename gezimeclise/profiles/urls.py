from django.conf.urls import patterns, url
<<<<<<< HEAD
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
=======
from gezimeclise.profiles.views import ProfileListView, ProfileDetailView, \
                                       ProfileUpdateView, ProfileSupport

urlpatterns = patterns('',
    url(r'^$', ProfileListView.as_view(), name="profile_list"),
    url(r'^update/$', ProfileUpdateView.as_view(), name="profile_update"),

    url(r'^support/$', ProfileSupport.as_view(), name="profile_support"),

    url(r'^(?P<username>[-\w]+)/$', ProfileDetailView.as_view(), name="profile_detail"),
)
>>>>>>> 00bbcb699f9a856ea4d6b764a18c065c33746fe4
