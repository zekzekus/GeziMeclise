# coding: utf-8
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_facebook.models import FacebookModel
from django.contrib.auth.models import AbstractUser, UserManager
from taggit.managers import TaggableManager
from django_facebook.models import FacebookUser

REPORTTOPICS = ((1, "FAKE ACCOUNT"),
                (2, "BAD LANGUAGE")),


class Region(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', blank=True, null= True)

    def __unicode__(self):
        return self.name


class GeziUser(AbstractUser, FacebookModel):
    supports = models.ManyToManyField('self', blank=True, symmetrical=False,
                                      related_name='supporters')
    causes = models.TextField(blank=True, null=True)
    tags = TaggableManager(blank=True)
    region = models.ForeignKey(Region, null=True)
    objects = UserManager()

    def get_facebook_friends(self):
        return FacebookUser.objects.filter(user_id=self.id).values('user_id')

    def get_registered_friends(self):
        return GeziUser.objects.filter(id__in=FacebookUser.objects.filter(
            user_id=self.id).values('user_id')).exclude(id=self.id)


class Report(models.Model):
    reporter = models.ForeignKey(GeziUser, related_name="reporter")
    reported = models.ForeignKey(GeziUser, related_name="reported")
    topic = models.IntegerField(choices=REPORTTOPICS)

    class Meta:
        unique_together = ('reporter', 'reported', 'topic')
    def __unicode__(self):
        return str(self.reporter + self.reported + self.topic)

    def deactivate_user(self):
        self.reporter.is_active=False
        self.reporter.save()


@receiver(post_save, sender=GeziUser)
def new_friend_notification_handler(sender, instance, **kwargs):
    from gezimeclise.notifications.models import Notification
    if kwargs['created']:
        for friend in instance.get_registered_friends():
            Notification.objects.create(sender=sender, receiver=friend,
                                        notification="supported")