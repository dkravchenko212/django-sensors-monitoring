#from django.shortcuts import render
import os
from django.views import generic
from django.conf import settings
from djangoapp.models import Measurement
from django.shortcuts import render

class MeasurementList (generic.ListView):
    model = Measurement
    context_object_name = 'measurements'
    template_name = 'measurement_list.html'
    
    def get(self, request, *args, **kwargs):
        values = Measurement.objects.all()
        return render(request, 'measurement_list.html', {'measurements': values})
