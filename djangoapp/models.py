from __future__ import unicode_literals
from django.db import models

class Measurement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    value = models.CharField(max_length=50)
    sensor_name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, null=True)
    
    def __unicode__(self):
        return self.value 

#mr = Measurement()
#mr.value = 'aertw'
#mr.description = 'do not buy lanos'
#mr.save()
