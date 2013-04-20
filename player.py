#!/usr/bin/python
from time import sleep
from general import DEBUG, PPQN
from automation import AutomationTrack, AutomationPhrase, AE
from score import ScoreTrack, ScorePhrase, SE

import pypm

msleep = lambda x: sleep(x/1000.0)

class Player:
  def debug_ShowMidiDevices(self):
    numDevices = pypm.CountDevices()
    for n in range(numDevices):
      print ("%d - %s") % (n, pypm.GetDeviceInfo(n))

  def __init__(self):
    self.tracks = []

  def addTrack(self, track):
    if (isinstance(track, AutomationTrack)):
      if (DEBUG):
        print "[ PLAYER   ] New automation track added"
    if (isinstance(track, ScoreTrack)):
      if (DEBUG):
        print "[ PLAYER   ] New score track added"
    self.tracks.append(track)

def main2():
  p = Player()
  a = AutomationTrack()
  s = ScoreTrack()

  s1 = ScorePhrase()
  s2 = ScorePhrase()
  s.addPhrase(s1, 0)
  s.addPhrase(s2, 1)
  s.setMidiTranspose(-12)
  
  # lead thing
  b = 12 * 6
  s1.addEvent(SE(b,   127,  0))
  s1.addEvent(SE(b,   127,  6))
  s1.addEvent(SE(b+7, 127, 12))
  s1.addEvent(SE(b+7, 127, 18))
  s1.addEvent(SE(b+9, 127, 24))
  s1.addEvent(SE(b+9, 127, 30))
  s1.addEvent(SE(b+7, 127, 36))

  s2.addEvent(SE(b+5, 127,  0))
  s2.addEvent(SE(b+5, 127,  6))
  s2.addEvent(SE(b+4, 127, 12))
  s2.addEvent(SE(b+4, 127, 18))
  s2.addEvent(SE(b+2, 127, 24))
  s2.addEvent(SE(b+2, 127, 30))
  s2.addEvent(SE(b+0, 127, 36))

  # automations
  a1 = AutomationPhrase()
  a.setMidiChannel(1)
  a.setCC(64)
  a1.addEvent(AE(0, 0))
  a1.addEvent(AE(127, 24))
  a.addPhrase(a1, 0)
  a.addPhrase(a1, 1)


  p.addTrack(a)
  p.addTrack(s)

  s.getLastBar()
  #p.debug_ShowMidiDevices()
  #return
  pypm.Initialize()
  m = pypm.Output(0, 0)
  m.WriteShort(0xB0, 99, 1)
  #m.WriteShort(0xB0, 52, 1)
  #m.WriteShort(0xB0, 71, 64)
  #m.WriteShort(0xB0, 76, 1)

  print "a=",a.getMidiAt(0,0)
  print "s=",s.getMidiAt(0,0)
  print "a=",a.getMidiAt(0,24)
  print "s=",s.getMidiAt(0,24)

  
  # for 2 bars
  for b in range(2):
    # for all 48 PPQN events
    for t in range(0, 47, 6):
      # for all tracks in the player
      for z in p.tracks:
        events = z.getMidiAt(b,t)
        if (events != None):
          print ("midi events on track [ %s ] at %d,%d: %s") % (z.getName(), b, t, events)
          n = events[0]
          if (n != None):
            m.WriteShort(n[0], n[1], n[2])
      msleep(200)

def main():
  a = ScorePhrase()
  a.addEvent(SE(60, 127,   0))
  a.addEvent(SE(55, 127,   9))
  a.addEvent(SE(52, 127,  18))
  a.addEvent(SE(57, 127,  27))
  a.addEvent(SE(59, 127,  33))
  a.addEvent(SE(57, 127,  39))
  a.addEvent(SE(56, 127,  42))

  track1 = ScoreTrack()
  track1.addPhrase(a, 0)
  track1.setMidiChannel(1)
  track1.setMidiTranspose(12)

  player = Player()
  player.addTrack(track1)

  #initialize midi
  pypm.Initialize()
  m = pypm.Output(0, 0)
  m.WriteShort(0xB0, 99, 1)
  m.WriteShort(0xB0, 74, 51)
  m.WriteShort(0xB0, 11, 82)
  m.WriteShort(0xB0, 75, 80)
  m.WriteShort(0xB0, 77, 72)
  m.WriteShort(0xB0, 71, 73)

  bpm = 120
  deltat = 60000.0/ bpm / 4 / 4
  print deltat
  # for 2 bars
  for b in range(2):
    # for all 48 PPQN events
    for t in range(0, 47, 1):
      # for all tracks in the player
      for z in player.tracks:
        events = z.getMidiAt(b,t)
        if (events != None):
          print ("midi events on track [ %s ] at %d,%d: %s") % (z.getName(), b, t, events)
          n = events[0]
          if (n != None):
            m.WriteShort(n[0], n[1], n[2])
      msleep(deltat)


main()
