#!/usr/bin/python
import math
import pypm
from general import PPQN


class AutomationTrack:
  def __init__(self):
    self.phrases = list()
    self.cc = 42          # default cc cause 42
    self.channel = 1
    self.automationPhrases = {} # needs a dictionary so we can have time sequences with empty 
    self.trackName = "Unnamed Automation Track"

  def addPhrase(self, automationPhrase, position):
    # TODO: replace existing phrase if one exists
    # self.automationPhrases.insert(automationPhrase)
    if (type(position) == int and position >= 0):
      print ("[ ATMATION ] Added APhrase at position %d") % (position)
      self.automationPhrases[position] = automationPhrase

  def setCC(self, value):
    self.cc = value

  def getCC(self, value):
    return self.cc

  def setMidiChannel(self, value):
    self.channel = value-1

  def getMidiChannel(self):
    return self.channel + 1

  def setName(self, value):
    self.trackName = value

  def getName(self):
    return self.trackName

  def simpleRender(self, phrase):
    #print ("Rendering phrase %d, %d events") % (phrase, len(self.automationPhrases[phrase].events))
    phrase = self.automationPhrases[phrase]

    #for e in events:
    #  print ("%d at %d") % (e.value, e.time)
    n = (0xB0 | self.channel, self.cc, phrase.events[2].value)
    print(n)

  def getMidiAt(self, bar, timeframe):
    # position is a PPQN index
    # phrase = self.automationPhrases[phraseID]
    phrase = self.automationPhrases.get(bar, None)
    if (phrase != None):
      eventValue = phrase.e2.get(timeframe, None)
      if (eventValue != None):
        result = list()
        result.append((0xB0 | self.channel, self.cc, eventValue))
        return result
      else:
        return None
    else:
      return None


class AutomationPhrase:
  def __init__(self):
    self.e2 = {}

  def addEvent(self, event):
    #print ("Added event %d at time %d") % (event.value, event.time)
    self.e2[event.time] = event.value

class AE: # automation event
  def __init__(self, value, time):
    self.time = time
    if (type(value) == float):
      value = int(128 * value)
    if (value < 0 or value > 127):
      value = 64
    self.value = value

def main():
  a = AutomationPhrase()
  for i in range(PPQN*4):
    # sin in the range of pi/2 (0 -> 1 following sin function), repeated once for each quarter note
    value = (math.sin((math.pi/2) * (i % PPQN) / PPQN))
    tempAE = AE(value, i)
    if (i%4 == 0):
      a.addEvent(tempAE)

  at = AutomationTrack()
  at.setMidiChannel(16)
  at.setCC(1)
  at.addPhrase(a, 3)
  #at.simpleRender(3)
  
  for i in range(16):
    print(at.getMidiAt(3, i))

# do some other debugging stuff if it's running standalone
if (__name__ == '__main__'):
  print "Running as a script"
  main()
