import wiringpi
import time
import sys
from wiringpi import GPIO

relay_1 = 3
relay_2 = 4

wiringpi.wiringPiSetup()
wiringpi.pinMode(relay_1, GPIO.OUTPUT)
wiringpi.pinMode(relay_2, GPIO.OUTPUT)

while True:
    try:
        wiringpi.digitalWrite(relay_1, GPIO.HIGH)
        time.sleep(0.5)
        wiringpi.digitalWrite(relay_1, GPIO.LOW)
        time.sleep(1)
        wiringpi.digitalWrite(relay_2, GPIO.LOW)
        time.sleep(0.5)
        wiringpi.digitalWrite(relay_2, GPIO.HIGH)
        time.sleep(0.5)
    except KeyboardInterrupt:
        wiringpi.digitalWrite(relay_1, GPIO.HIGH)
        wiringpi.digitalWrite(relay_2, GPIO.HIGH)
        sys.exit(0)
