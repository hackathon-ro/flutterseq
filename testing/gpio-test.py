#!/usr/bin/python

import RPi.GPIO as GPIO
import time
p = 18

def main():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(p, GPIO.OUT)
  while(1):
    for i in range(10):
      for n in range(10):
        GPIO.output(p, GPIO.HIGH)
        time.sleep(0.020 * i/3)
        GPIO.output(p, GPIO.LOW)
        time.sleep(0.020 * i/3)

try:
  main()
except KeyboardInterrupt:
  GPIO.cleanup()
