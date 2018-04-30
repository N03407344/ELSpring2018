#!/usr/bin/env python3
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def setServoAngle(servo, angle):
    assert angle >= 0 and angle <= 180
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    duty = (angle / 18.) + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.3)
    pwm.stop()



if __name__ == '__main__':
        import sys
        servo = int(sys.argv[0])
        GPIO.setup(servo, GPIO.OUT)
        setServoAngle(servo, int(sys.argv[1]))
        GPIO.cleanup()
