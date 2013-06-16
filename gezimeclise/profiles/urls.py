from django.conf.urls import patterns, include, url
from gezimeclise.profiles.views import ProfileListView

urlpatterns = patterns('',
                       url(r'^$', ProfileListView.as_view(),
                           name="profile_list"),
                       )
