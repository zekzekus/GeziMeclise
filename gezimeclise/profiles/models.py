from django.db import models
from django_facebook.models import FacebookModel


try:
    from django.contrib.auth.models import AbstractUser, UserManager
    
    class GeziUser(AbstractUser, FacebookModel):
        objects = UserManager()
        
        supports = models.ManyToManyField('self', blank=True)
except ImportError, e:
    print 'Couldnt setup FacebookUser, got error %s', e
