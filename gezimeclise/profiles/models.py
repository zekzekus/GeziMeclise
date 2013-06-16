from django.db import models
from django_facebook.models import FacebookModel
from django.contrib.auth.models import AbstractUser, UserManager


class GeziUser(AbstractUser, FacebookModel):
    supports = models.ManyToManyField('self', blank=True)

    objects = UserManager()
