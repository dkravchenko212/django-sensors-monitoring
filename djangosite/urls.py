"""djangosite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.urls import re_path as url
from django.contrib import admin
from django.urls import path
from djangoapp.views import MeasurementList, switch_relay

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('', MeasurementList.as_view(), name='measurement_list'),
    path('switch-relay/', switch_relay, name='switch-relay')
]


#==================================================
# Used to start scheduled jobs
# import file or directly paste the contents of execute.py
#==================================================
import execute