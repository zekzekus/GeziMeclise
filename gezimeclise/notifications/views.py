from django.views.generic import ListView
from gezimeclise.notifications.models import Notification


class NotificationsList(ListView):
    template_name = "notifications/notification_list.html"
    context_object_name = "notification_list"

    def get_queryset(self):
        return Notification.objects.for_me(self.request.user)