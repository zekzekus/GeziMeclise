#coding="utf-8"
from django.db import models
from gezimeclise.profiles.models import GeziUser


NOTIFICATIONS_TYPE_NEW_USER = 0
NOTIFICATIONS_TYPE_SUPPORT = 1

NOTIFICATIONS_CHOICES = (
    (NOTIFICATIONS_TYPE_NEW_USER, "New User"),
    (NOTIFICATIONS_TYPE_SUPPORT, "Supported"),
)

NOTIFICATION_TEMPLATES = {
    NOTIFICATIONS_TYPE_NEW_USER: "%(username)s is now here.",
    NOTIFICATIONS_TYPE_SUPPORT: "%(username)s is supporting you now.",
}


class NotificationManager(models.Manager):

    def for_me(self, user):
        """Returns notification of user"""
        return self.get_query_set().filter(receiver=user)


class Notification(models.Model):
    sender = models.ForeignKey(GeziUser, related_name="sender")
    receiver = models.ForeignKey(GeziUser, related_name="receiver")
    notification = models.IntegerField(choices=NOTIFICATIONS_CHOICES, max_length=255)
    read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = NotificationManager()

    class Meta:
        ordering = ["read", "-date_created"]

    def __unicode__(self):
        return "%s: %s" % (self.receiver.username, self.as_text())

    def as_text(self):
        return NOTIFICATION_TEMPLATES[self.notification] % {
            "username": self.sender.username
        }

    def mark_as_read(self):
        self.read = True
        self.save()
    mark_as_read.alters_data = True
