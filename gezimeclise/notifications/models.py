#coding="utf-8"
from django.db import models
from gezimeclise.profiles.models import GeziUser


NOTIFICATIONS_TYPE_NEW_USER = "new user"
NOTIFICATIONS_TYPE_SUPPORT = "supported"

NOTIFICATIONS = ((NOTIFICATIONS_TYPE_NEW_USER, "NEW USER is here"),
                 (NOTIFICATIONS_TYPE_SUPPORT, "YOU ARE SUPPORTED by"))


class Notification(models.Model):
    sender = models.ForeignKey(GeziUser, related_name="sender")
    receiver = models.ForeignKey(GeziUser, related_name="receiver")
    notification = models.CharField(choices=NOTIFICATIONS, max_length=255)
    read = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.sender.username + self.receiver.username +
                   self.notification + self.id)