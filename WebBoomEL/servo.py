#!/usr/bin/env python3

import sys
import os
import time
import RPi.GPIO as GPIO

def main(argv):
     start = argv[1]
     end = argv[2]
     delay = argv[3]
     loop = argv[4]
     GPIO.setmode(GPIO.BOARD)
     GPIO.setwarnings(False)
     GPIO.setup(11, GPIO.OUT)
     GPIO.setup(13, GPIO.OUT)
     p = GPIO.PWM(11, 100)
     p1 = GPIO.PWM(13, 100)
     p.start(0)
     p1.start(0)
     for i in range(0, int(loop)):
             for j in range(int(start), int(end), 1):
		   p.ChangeDutyCycle(j)
		   p1.ChangeDutyCycle(j)
		   print j
		   time.sleep(float(delay))
	     for j in range(int(end), int(start), -1):
		   p.ChangeDutyCycle(j)
		   p1.ChangeDutyCycle(j)
		   print j
		   time.sleep(float(delay))
     p.stop()
     p1.stop()
     GPIO.cleanup()

if __name__ == "__main__":
	 if len(sys.argc) < 5:
			print "servo.py <start> <end> <delay> <loop>"
	 else:
		main(sys.argv)
