#!/usr/bin/env python3
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def setServoAngle(servo):
    pwm = GPIO.PWM(servo, 50)
    pwm.start(0)
    pwm.ChangeDutyCycle(2)
    sleep(0.3)
    pwm.stop()




if __name__ == '__main__':
        import sys
        servo = int(sys.argv[1])
        GPIO.setup(servo, GPIO.OUT)
        setServoAngle(servo)
        GPIO.cleanup()
