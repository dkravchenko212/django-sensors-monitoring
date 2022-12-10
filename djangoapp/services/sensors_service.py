from enum import Enum
import time
import sys
from typing import Any, Tuple, List
import wiringpi
from wiringpi import GPIO


class SwitchState(Enum):
    ON = 1
    OFF = 0

class SensorsService(object):
    instance = None
    dht_pin = 6
    relay_1_pin = 3
    relay_2_pin = 4
    relay_state = SwitchState.ON
    
    def __new__(cls):
        if cls.instance is not None:
            return cls.instance
        else:
            inst = cls.instance = super(SensorsService, cls).__new__(cls)
            return inst
    
    def get_data_from_dht11(self) -> Tuple[float, float]:
        temp,hum = self.__parse_value_from_dth11()
        return (temp, hum)
    
    def get_data_from_camera(self) -> Any:
        pass
    
    def trigger_relay(self) -> None:
        if self.relay_state.value == 1:
            self.switch_relay(1, SwitchState.OFF)
        else:
            self.switch_relay(1, SwitchState.ON)
        
    def switch_relay(self, number: int=1, state: SwitchState=SwitchState.ON) -> Any:
        res: int = -1
        if number == 1:
            res = self.__set_relay_state(self.relay_1_pin, state)
        elif number == 2:
            res = self.__set_relay_state(self.relay_2_pin, state)
        else:
            print("ERROR: Cannot switch relay.\nWrong relay number {} (possible values 1,2)".format(number))
        if res != -1:
            print("Successfully switched relay {} to state {}".format(number, state.name))

    def __read_value_from_dht11(self) -> List[int]:
        tl=[]
        tb=[]
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(self.dht_pin, GPIO.OUTPUT)
        wiringpi.digitalWrite(self.dht_pin, GPIO.HIGH)
        wiringpi.delay(1)
        wiringpi.digitalWrite(self.dht_pin, GPIO.LOW)
        wiringpi.delay(25)
        wiringpi.digitalWrite(self.dht_pin, GPIO.HIGH)
        wiringpi.delayMicroseconds(20)
        wiringpi.pinMode(self.dht_pin, GPIO.INPUT)
        while(wiringpi.digitalRead(self.dht_pin)==1): pass

        for i in range(45):
            tc=wiringpi.micros()
            while(wiringpi.digitalRead(self.dht_pin)==0): pass
            while(wiringpi.digitalRead(self.dht_pin)==1):
                if wiringpi.micros()-tc>500:
                    break
            if wiringpi.micros()-tc>500:
                break
            tl.append(wiringpi.micros()-tc)

        tl=tl[1:]
        for i in tl:
            if i>100:
                tb.append(1)
            else:
                tb.append(0)

        return tb


    def __parse_value_from_dth11(self) -> Tuple[float,float]:
        SH=0;SL=0;TH=0;TL=0;C=0
        temperature = 0
        humidity = 0
        result=self.__read_value_from_dht11()

        if len(result)==40:
            for i in range(8):
                SH*=2;SH+=result[i]    # humi Integer
                SL*=2;SL+=result[i+8]  # humi decimal
                TH*=2;TH+=result[i+16] # temp Integer
                TL*=2;TL+=result[i+24] # temp decimal
                C*=2;C+=result[i+32]   # Checksum
            if ((SH+SL+TH+TL)%256)==C and C!=0:
                temperature = float("{}.{}".format(TH,TL))
                humidity = float("{}.{}".format(SH,SL))
                return temperature, humidity
            else:
                print("Read was successful,but there is checksum mismatch")

        else:
            print("Read failed!")
        wiringpi.delay(200)
        return temperature, humidity

    def __set_relay_state(self, pin: int, state: SwitchState) -> int:
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(pin, GPIO.OUTPUT)
        if state.value == 1:
            wiringpi.digitalWrite(pin, GPIO.HIGH)
            return 1
        elif state.value == 0:
            wiringpi.digitalWrite(pin, GPIO.LOW)
            return 0
        else:
            print("ERROR: Wrong switch state {}".format(state.value))
            return -1
