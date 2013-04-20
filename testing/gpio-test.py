#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from time import sleep

msleep = lambda x: sleep(x/1000.0)
p = 16

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

# testing HC165 PISO register
# HEADER PIN 3 - OUTPUT - SHIFT/LOAD
# HEADER PIN 5 - OUTPUT - CLOCK
# HEADER PIN 7 - INPUT  - DATA

P_LOAD = 3
P_CLOCK= 5
P_DATA = 7

def main2():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(P_LOAD, GPIO.OUT)
  GPIO.setup(P_CLOCK, GPIO.OUT)
  GPIO.setup(P_DATA, GPIO.IN)

  # pulse load signal
  GPIO.output(P_LOAD, 1)
  msleep(0.1)
  GPIO.output(P_LOAD, 0)
  msleep(0.1)
  GPIO.output(P_LOAD, 1)

  dataIn = list()
  for i in range(10):
    GPIO.output(P_CLOCK, 0)
    msleep(0.1)
    GPIO.output(P_CLOCK, 1)
    msleep(0.1)

    temp = GPIO.input(P_DATA)
    dataIn.append(temp)

  print (dataIn)

try:
  main2()
except KeyboardInterrupt:
  GPIO.cleanup()
