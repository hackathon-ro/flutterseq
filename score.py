#!/usr/bin/python
from general import PPQN, DEBUG

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

# this will be an include later, but for now, we test it as a standalone item
if (__name__ == '__main__'):
  print "Running as a script"
  main()
