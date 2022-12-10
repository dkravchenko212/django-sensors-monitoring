from djangoapp.services.sensors_service import SensorsService, SwitchState
from djangoapp.models import Measurement
import time
   
def update_data_from_sensors():
    sensors = SensorsService()
    res = sensors.get_data_from_dht11()
    print("Data from DHT11 : {}".format(res))
    if res[0] != 0:
        print("Saving measurement from DHT11")
        mr = Measurement()
        mr.sensor_name = "DHT11"
        mr.value = "Temperature: {} Humidity: {}".format(res[0], res[0])
        mr.description = "sensor connected to orangepi 3 lts"
        mr.save()
        print("Done saving")

