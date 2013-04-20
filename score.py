#!/usr/bin/python
from general import PPQN, DEBUG

class ScoreTrack:
  def __init__ (self):
    self.phrases = {}
    self.channel = 0
    self.trackName = "Unnamed Score Track"
    self.midiTranspose = 0

  def setMidiTranspose(self, value):
    self.midiTranspose = value

  def setMidiChannel(self, value):
    if (value >= 1 and value <= 16):
      self.channel = value - 1

  def setName(self, value):
    self.trackName = value

  def getName(self):
    return self.trackName

  def getMidiChannel(self, value):
    return self.channel + 1

  def getLastBar(self):
    a = self.phrases.keys()
    print a

  def addPhrase(self, phrase, bar):
    # check if there's already a phrase at the required position
    if (self.phrases.get(bar, None) != None):
      if (DEBUG == 1):
        print ("Replacing phrase at bar %d") % (bar)

    self.phrases[bar] = phrase

  def getMidiAt(self, bar, timeframe):
    phrase = self.phrases.get(bar, None)
    if (phrase != None):      # check if the bar has an associated phrase on the track
      if (phrase.events.get(timeframe) != None):  # the phrase must have a SE list at the required timeframe
        event = phrase.events[timeframe]
        result = list()
        if (DEBUG):
          pass
          #print "Events at %d,%d:" % (bar, timeframe),
        for e in event:
          if (DEBUG):
            pass
            #print ("%3d, ") % (e.note),
          #temp = (0x90 | self.channel, e.note, e.velocity)
          note = e.note
          note+=self.midiTranspose
          if (note < 0):
            note = 0
          if (note > 127):
            note = 127
          temp = (0x90, note, e.velocity)
          result.append(temp)
        if (DEBUG):
          print
        return result
      else:
        return None
    else:
      return None

class ScorePhrase:
  def __init__ (self):
    self.events = {}

  def addEvent(self, event):
    position = event.start
    # if this is the first note of a chord, make a list so we can store all subsequent notes of the chord here
    if (self.events.get(position, None) == None):
      self.events[position] = list()
    
    # check to see if this is unique. No reason in having twice the same note on the same track
    for e in self.events[position]:
      if (e.note == event.note):
        if (DEBUG):
          print ("Did not add score event to score phrase, an event with the same pitch already exists at the same position")
          return

    # well, we can add it now
    self.events[position].append(event)

class SE: #Score Event
  def __init__ (self, note, velocity, start, duration=None):
    self.note = note
    self.velocity = velocity
    self.start = start
    self.duration = duration

def main():
  a = ScorePhrase()
  a.addEvent(SE(40, 127, 0))
  a.addEvent(SE(45,  64, 0))
  a.addEvent(SE(48,  64, 0))
  a.addEvent(SE(48,  32, 24))
  a.addEvent(SE(49,  64, 24))

  b = ScoreTrack()
  b.addPhrase(a, 1)
  print b.getMidiAt(1, 0)
  print b.getMidiAt(1, 24)

if (__name__ == '__main__'):
  print "Running as a script"
  main()
