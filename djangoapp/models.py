from __future__ import unicode_literals
from django.db import models

class Measurement(models.Model):
    value = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True, null=True)
    
    def __unicode__(self):
        return self.value 

#mr = Measurement()
#mr.value = 'aertw'
#mr.description = 'do not buy lanos'
#mr.save()
