#!/usr/bin/env python3
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#method moves continuous servo to the left
def SetAngle(servo):
     pwm = GPIO.PWM(servo,50)
     pwm.start(0)
     pwm.ChangeDutyCycle(8)
     sleep(0.3)
     pwm.stop()

if __name__ == '__main__':
     import sys
     servo = int(sys.argv[1])
     GPIO.setup(servo, GPIO.OUT)
     SetAngle(servo)
     GPIO.cleanup()
