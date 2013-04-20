#!/usr/bin/python
# flutterseq, 2013-04-20, raspberry pi hackathon
# first test, midi message library

import pypm

def main():
  print "Initialize"
  pypm.Initialize()
  m = pypm.Output(0, 0)

  print "Send C4"
  m.WriteShort(0x90, 0x40, 0x7F);

main()
