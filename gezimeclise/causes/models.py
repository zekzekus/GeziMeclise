from django.db import models
from gezimeclise.profiles.models import GeziUser, Region


class Cause(models.Model):
    description = models.TextField()
    user = models.ForeignKey(GeziUser)
    supporters = models.ManyToManyField(GeziUser, related_name='supported_causes', blank=True)
    region = models.ForeignKey(Region, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
