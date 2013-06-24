from gezimeclise.notifications.views import NotificationsList
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    # notication_urls
    url(r'^$', NotificationsList.as_view(), name="notifications"))

