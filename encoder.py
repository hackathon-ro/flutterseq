#!/usr/bin/python

class Encoder:
  def __init__(self, reverse = False):
    self.a = bool(0)
    self.b = bool(0)
    self.oa = bool(0)
    self.ob = bool(0)
    self.position = 0
    self.reverse = reverse

  def update(self, a, b):
    if (self.a != self.oa or self.b != self.ob):
      #print ("Val %1d-%1d") % (a,b)
      if (self.reverse == True):
        direction = self.a ^ self.ob
      else:
        direction = self.b ^ self.oa

      if (direction == 1):
        self.position += 1
      elif (direction == 0):
        self.position -= 1
      #print "Dir", direction
      print "Pos", self.position
      #print 

    self.oa = self.a
    self.ob = self.b
    self.a = a
    self.b = b

  def reset(self):
    self.position = 0
