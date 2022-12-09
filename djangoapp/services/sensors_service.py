from enum import Enum
from typing import Any, Tuple


class SwitchState(Enum):
    ON = 1
    OFF = 0

class SensorsService(object):
    instance = None
    
    def __new__(cls):
        if cls.instance is not None:
            return cls.instance
        else:
            inst = cls.instance = super(SensorsService, cls).__new__(cls)
            return inst
    
    def get_data_from_dht11(self) -> Tuple[float, float]:
        return (4.5, 10.2)
    
    def get_data_from_camera(self) -> Any:
        pass
    
    def switch_relay(self, number: int=1, state: SwitchState=SwitchState.ON) -> Any:
        print("switched BEACH")
    

