from django.conf.urls import patterns, url

from gezimeclise.blog.views import (BlogDetailView, BlogIndexView,
                                    BlogPostsRssFeed, BlogPostsAtomFeed,
                                    BlogUpdateView, BlogCreateView)


urlpatterns = patterns('',

    # blog urls
    url(r'^$', BlogIndexView.as_view(), name="blog"),
    url(r'^blog/(?P<slug>[-\w]+)/$', BlogDetailView.as_view(), name="blog_detail"),
    url(r'^update/(?P<slug>[-\w]+)/$', BlogUpdateView.as_view(),name="blog_update"),
    url(r'^create/$', BlogCreateView.as_view(),name="blog_create"),
    url(r'^$', BlogIndexView.as_view(), name="blog_index"),
    url(r'^(?P<slug>[-\w]+)/$', BlogDetailView.as_view(), name="blog_detail"),


    # rss & atom feed
    url(r'^feed/rss$', BlogPostsRssFeed(), name="blog_rss_feed"),
    url(r'^feed/atom', BlogPostsAtomFeed(), name="blog_atom_feed"),)


