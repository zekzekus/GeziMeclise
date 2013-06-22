from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_facebook.models import FacebookModel
from django.contrib.auth.models import AbstractUser, UserManager
from taggit.managers import TaggableManager
from django_facebook.models import FacebookUser
from gezimeclise.notifications.models import Notification


class GeziUser(AbstractUser, FacebookModel):
    supports = models.ManyToManyField('self', blank=True, symmetrical=False,
                                      related_name='supporters')
    causes = models.TextField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    objects = UserManager()

    def get_facebook_friends(self):
        return FacebookUser.objects.filter(user_id=self.id).values('user_id')

    def get_registered_friends(self):
        return GeziUser.objects.filter(id__in=FacebookUser.objects.filter(
            user_id=self.id).values('user_id')).exclude(id=self.id)


@receiver(post_save, sender=GeziUser)
def new_friend_notification_handler(sender, **kwargs):
    if kwargs['created']:
        for friend in sender.get_registered_friends():
            Notification.objects.create(sender=sender, receiver=friend,
                                        notification="supported")