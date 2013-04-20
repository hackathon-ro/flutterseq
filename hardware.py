#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
msleep = lambda x: sleep(x/1000.0)

class InShifter():
  def __init__(self, clockPin, dataPin, loadPin):
    self.p_clock = clockPin
    self.p_data  = dataPin
    self.p_load  = loadPin

    #setup gpio TODO: does it work while being instanced?
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.p_clock, GPIO.OUT)
    GPIO.setup(self.p_data,  GPIO.IN)
    GPIO.setup(self.p_load,  GPIO.OUT)

  def readBit(self):
    # bool casted value depending on current serial bit
    x = GPIO.input(self.p_data)
    if (x):
      return 1
    else:
      return 0

  def shift16(self):
    # TODO: make it more generic, currently we have 3 x 16 bit HC165 shifters

    # this is horrible, but it works. and there's only 10:58 left
    # load buffers
    GPIO.output(self.p_load, 0)
    msleep(0.1)
    GPIO.output(self.p_load, 1)
    msleep(0.1)

    # clock 16 bits in
    bits = list()
    for i in range(16):
      bit = self.readBit()
      bits.append(bit)
      GPIO.output(self.p_clock, 0)
      msleep(0.1)
      GPIO.output(self.p_clock, 1)
      msleep(0.1)
    return bits

def main():
  i = InShifter(5, 7, 3)
  while(1):
    print i.shift16()
    msleep(50)

try:
  main()
except KeyboardInterrupt:
  GPIO.cleanup()
