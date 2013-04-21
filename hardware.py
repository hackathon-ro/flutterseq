#!/usr/bin/python
from encoder import Encoder
import RPi.GPIO as GPIO
from time import sleep
msleep = lambda x: sleep(x/1000.0)

# InShifter - clocks bits out of hc165
# EncoderInterface - parses data from an InShifter into quadrature encoder positions. clock/data/load pins hardcoded here (TODO: shouldn't do that)
#   TODO: add event chain
# ButtonInterface - parses data from two InShifters into basic button events

EVENT_BUTTONPRESS = 0
EVENT_BUTTONRELEASE = 1

class ButtonInterface():
  def __init__(self):
    self.events = list()
    # create blank current/previous lists for button states
    self.old = [0] * 32
    self.new = [0] * 32
    self.count = 0
  
  def readHardware(self):
    self.old = self.new
    self.new = self.fakeRead()
    for (k, p) in enumerate(self.new):
      #print (p),
      if (self.new[k] == 1 and self.old[k] == 0):
        # button pressed
        #print "x",
        print "[ BtnIface ] Button %d pressed" % k
        self.events.add((EVENT_BUTTONPRESS), k)
      elif (self.new[k] == 0 and self.old[k] == 1):
        # button released
        #print "o",
        print "[ BtnIface ] Button %d released" % k
        self.events.add((EVENT_BUTTONRELEASE), k)

      #else:
      # no event on this button
      #  print "-",
    print 

  def fakeRead(self):
    #because hardware is still in development
    self.count += 1
    if (self.count == 1 or self.count == 3):
      return ([1] * 2) + ([0] * 30)
    elif (self.count == 2 or self.count == 4):
      return ([0] * 31 + [1] * 1)
    
    else:
      return ([0] * 32)
    

class EncoderInterface():
  def __init__(self):
    self.encoders = [0,0,0,0,0,0,0,0]
    self.shifter = InShifter(5, 7, 3)
    self.old = list()
    self.new = list()
    self.encoderInstances = list()
    for i in range(16):
      self.old.append(0)
      self.new.append(0)
      if (i%2 == 0):
        self.encoderInstances.append(Encoder())

  def readHardware(self):
    self.old = self.new
    self.new = self.shifter.shift16()
    for i in range(0,4,2):
      result = self.encoderInstances[i/2].update(self.new[i], self.new[i+1])
      if (result):
        print "Encoder %d: %d" % (i/2, self.encoderInstances[i/2].position)

class InShifter():
  def __init__(self, clockPin, dataPin, loadPin):
    self.p_clock = clockPin
    self.p_data  = dataPin
    self.p_load  = loadPin

    #setup gpio TODO: does it work under multiple instances?
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

class OutShifter():
  def __init__(self, clockPin, dataPin, loadPin):
    self.p_clock = clockPin
    self.p_data  = dataPin
    self.p_load  = loadPin
    #setup gpio 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.p_clock, GPIO.OUT)
    GPIO.setup(self.p_data,  GPIO.OUT)
    GPIO.setup(self.p_load,  GPIO.OUT)
  
  def shift24(self, data):
    for i in range(8):
      GPIO.output(self.p_data, data[i])
      GPIO.output(self.p_clock, 0)
      msleep(0.1)
      GPIO.output(self.p_clock, 1)
      msleep(0.1)
    GPIO.output(self.p_load, 0)
    msleep(0.1)
    GPIO.output(self.p_load, 1)
    msleep(0.1)
      

def main2():
  #i = InShifter(5, 7, 3)
  #while(1):
  #  print i.shift16()
  #  msleep(50)

  eii = EncoderInterface() #encoderInterface instance
  while(1):
    eii.readHardware()
  msleep(5)


def main():
  i = OutShifter(13, 15, 11)
  while(1):
    i.shift24([0] * 1 + [1] * 1 + [0] * 6)
    msleep(500)
    i.shift24([0] * 1 + [0] * 1 + [0] * 6)
    msleep(500)
  #b = ButtonInterface()
  #b.readHardware()
  #b.readHardware()
  #b.readHardware()
  #b.readHardware()
  #b.readHardware()

try:
  main()
except KeyboardInterrupt:
  GPIO.cleanup()
