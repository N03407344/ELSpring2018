#!/usr/bin/env python3
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
panPin = 17
GPIO.setup(panPin, GPIO.OUT)
pan = GPIO.PWM(panPin, 50)
pan.start(0)
pan.ChangeDutyCycle(2)
pan.stop()
GPIO.cleanup()
