#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 15:50:43 2021

@author: michaelmitschjr
"""
import curses
import RPi.GPIO as GPIO
from AlphaBot2 import AlphaBot2
from TRSensors import TRSensor
import time

import random

def my_raw_input(stdscr, r, c, prompt_string): #I grabbed this function from stack overflow https://stackoverflow.com/questions/21784625/how-to-input-a-word-in-ncurses-screen
    curses.echo() 
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr(r + 1, c, 20)
    return input
 
def overscoreString(string):
   newString = ""
   for char in string:
      newString += "u'"+char+"\u0305'"  
   retString = ""
   for i in newString:
      if i != 'u' and i != "'":
         retString += i
   return retString

def getRobotPosition(pos):
   retString = ""
   div = 10
   incr = 4000/div
   for i in range(0, (div-1)):
      if (-2000+(incr*i))<pos and pos<(-2000+(incr*(i+1)):
         retString += "O"
      else:
         retString += "_"
   return retString

def main(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)
    
    #values = [10,150,70,90,110]
    freq = 5
	bot = botPosition()

    while True:

        stdscr.erase()

        max_y, max_x = stdscr.getmaxyx()
        max_y-=9 #3 lines for more info
        max_x-=1
        frequencyLine = max_y+3
        positionLine = max_y+4
        computedCenterLine = max_y+5
        newFreqLine = max_y+6

        bin_width = int(max_x//len(values))

        #for i in range(len(values)):
        #   values[i] += random.randint(0,10)
		values[i] = bot.sensorValues()
		pos = bot.position()

        stdscr.addstr(max_y+1,0, "\u203e"*max_x)

        for i in range(len(values)):
           height = max_y-int(max_y*(values[i]/max(values)))
           stdscr.addstr(max_y+1,i*bin_width+1,overscoreString("SENSOR "+str(i+1)))
           stdscr.addstr(height+1,i*bin_width+1,str(values[i]))
           try:
               for j in range(max_y-height):
                  stdscr.addstr(max_y-j, i*bin_width, "|")
                  stdscr.addstr(max_y-j, (i+1)*bin_width,"|")
               for j in range(bin_width):
                  stdscr.addstr(height,bin_width*i+j,"_")
               
           except:
               stdscr.addstr(0, 0, "oops")
        stdscr.addstr(frequencyLine,0, "Sample Frequency: "+str(freq)+" Hz")
        stdscr.addstr(positionLine,0, "Robot Relative to line: "+getRobotPosition(pos))
        
		stdscr.addstr(computedCenterLine,0, "Robot Computed Center Position: ")

        stdscr.refresh()

        key = stdscr.getch()

        # Process the keystroke
        if key == curses.KEY_RIGHT:
            continue
        if key == ord('f'): #typing f promts for new frequency
           freq = str(int(my_raw_input(stdscr, newFreqLine, 0, "new freq?")))
        elif key == ord('q'):
            break

curses.wrapper(main)

class botPosition:
	def __init__(self):
		self.Ab = AlphaBot2()
		self.TR = TRSensors()
		self.TR.calibrate()
		self.position, self.sensors
	
	def sensorValues(self):
		self.sensors = self.TR.readCalibrated()
		
		return self.sensors
		
	def onLine(self):
		self.sensors = self.TR.readCalibrated()
		lineValue = self.sensors
		for i in (0, self.sensors.length())
			if(self.sensors[i]>200):
				lineValue[i] = 1
			else:
				lineValue[i] = 0
		return lineValue
		
	def position(self):
		self.position, self.sensors = (self.TR.readLine() - 2000)
		return self.position