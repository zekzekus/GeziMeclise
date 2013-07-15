from gezimeclise.causes.views import (CausesListView, CauseCreateView,
                                      CauseDetailView, CauseSupportView,
                                      TagsList, CommentDeleteView)

from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', CausesListView.as_view(), name="cause_list"),
    url(r'^talep_yarat/$', CauseCreateView.as_view(), name="cause_create"),
    url(r'tags/gettag/$', TagsList.as_view(), name="tag_list"),
    url(r'^destek/$', CauseSupportView.as_view(), name="cause_support"),
    url(r'^delete_comment/$', CommentDeleteView.as_view(), name="delete_comment"),
    url(r'^(?P<slug>[-\w]+)/$', CauseDetailView.as_view(), name="cause_detail"),
)
