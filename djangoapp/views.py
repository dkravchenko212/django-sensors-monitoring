#from django.shortcuts import render
import os
from django.views import generic
from django.conf import settings
from djangoapp.models import Measurement

class MeasurementList (generic.ListView):
    model = Measurement
    context_object_name = 'measurements'
    template_name = 'measurement_list.html'
    
    def get(self, request, *args, **kwargs):
        try:
            file_path = os.path.join(settings.BASE_DIR, 'test_data')
            measurement_file = open(file_path, 'r')
            
            for value in measurement_file:
                Measurement.object.get_or_create(value=value)
        except IOError:
                pass
        return super(MeasurementList, self).get(request, *args, **kwargs)
