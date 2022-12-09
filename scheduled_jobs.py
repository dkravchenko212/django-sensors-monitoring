from djangoapp.services.sensors_service import SensorsService, SwitchState
import time

def cron_test():
    print("It works!")
    
def update_data_from_sensors():
    sensors = SensorsService()
    res = sensors.get_data_from_dht11()
    print("Data from DHT11 : {}".format(res))
    print("Switching relay state OFF")
    sensors.switch_relay(state=SwitchState.OFF)
    time.sleep(1)
    print("Switching relay state ON")
    sensors.switch_relay(state=SwitchState.ON)
    time.sleep(1)

