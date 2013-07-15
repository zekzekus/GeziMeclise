from django.db import models
from gezimeclise.profiles.models import GeziUser, Region
from taggit.managers import TaggableManager
from gezimeclise.utils import slugify


class Cause(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(GeziUser)
    supporters = models.ManyToManyField(GeziUser, related_name='supported_causes', blank=True)
    region = models.ForeignKey(Region, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    slug = models.SlugField()
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Cause, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title[:10]


class Comments(models.Model):
    cause = models.ForeignKey(Cause)
    commenter = models.ForeignKey(GeziUser, related_name="commenter")
    supporters = models.ManyToManyField(
        GeziUser, related_name="comment_supporters", blank=True, null=True)
    dislikers = models.ManyToManyField(
        GeziUser, related_name="disliklers", blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    class Meta:
        unique_together = ('cause', 'commenter')
        verbose_name_plural = "comments"

    def __unicode__(self):
        return self.comment[:10]
