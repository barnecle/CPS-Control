
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 15:50:43 2021

@author: michaelmitschjr
"""
import curses
import RPi.GPIO as GPIO
from python.AlphaBot2 import AlphaBot2
from python.TRSensors import TRSensor
import time

import random

class botPosition:
    def __init__(self):
        self.Ab = AlphaBot2()
        self.TR = TRSensor()
        self.Ab.stop()
        time.sleep(0.5)
        for i in range(0,100):
            if(i<25 or i>= 75):
                self.Ab.right()
                self.Ab.setPWMA(30)
                self.Ab.setPWMB(30)
            else:
                self.Ab.left()
                self.Ab.setPWMA(30)
                self.Ab.setPWMB(30)
        self.TR.calibrate()
        self.Ab.stop()

        self.TR.calibrate()
        self.position, self.sensors = self.TR.readLine()

    def sensorValues(self):
        #self.sensors = self.TR.readCalibrated()
        self.sensors = self.TR.AnalogRead()
        return self.sensors


    def getPosition(self):
        self.position, self.sensors = self.TR.readLine()
        return (self.position-2000)


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

def getRobotPosition(pos, lastString):
   retString = ""
   div = 10
   incr = 4000/div
   for i in range(0, (div-1)):
      if (2000-(incr*i))>pos and pos>(2000-(incr*(i+1))):
         retString += "O"
      else:
         retString += "_"
   if "O" in retString:
      return retString
   else:
      return lastString


def main(stdscr):

    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
   # stdscr.keypad(True)
    
    values = [0,0,0,0,0]
    freq = 1
    bot = botPosition()
    posString = " "

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
        values = bot.sensorValues()
        pos = bot.getPosition()

        stdscr.addstr(max_y,0, "_"*max_x)

        for i in range(len(values)):
           if max(values) == 0:
              height = max_y-1
           else:
              height = max_y-int(max_y*(values[i]/max(values)))
              if height == max_y: # want space to display value
                  height = max_y-1
           stdscr.addstr(max_y+1,i*bin_width+1,"SENSOR "+str(i+1))
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
        posString = getRobotPosition(pos, posString)
        stdscr.addstr(positionLine,0, "Robot Relative to line: "+posString)
        
        stdscr.addstr(computedCenterLine,0, "Robot Computed Center Position: ")
        time.sleep((1/freq))
        stdscr.refresh()

      #  key = stdscr.getch()

        # Process the keystroke
   #     if key == curses.KEY_RIGHT:
    #        continue
       # if key == ord('f'): #typing f promts for new frequency
        #   freq = str(int(my_raw_input(stdscr, newFreqLine, 0, "new freq?")))
       # elif key == ord('q'):
       #     break

curses.wrapper(main)

