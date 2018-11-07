#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pin = 4

def callBackTest(channel):
    print("callback")

GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(pin, GPIO.FALLING, callback=callBackTest, boucetime=300)

try:
    while(True):
        time.sleep(1)

except KeyboardInterrupt:
    print("break")
    GPIO.cleanup()
