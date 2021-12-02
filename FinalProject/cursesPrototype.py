#import RPi.GPIO as GPIO
#import time
#from AlphaBot2 import AlphaBot2
import curses


Ab = AlphaBot2()

def main(stdscr):
   curses.noecho()
   curses.cbreak()
   curses.curs_set(0)
   stdscr.keypad(True)
   while(True):
      stdscr.erase()
      key = stdscr.getch()
      if key == ord('w'):
         Ab.forward();
         print("up")
      elif key == ord('a'):
         Ab.left();
         print("left")
      elif key == ord('s'):
         Ab.backward();
         print("backward")
      elif key == ord('d'):
         Ab.right();
         print("right")
      elif key == ord(' '):
         Ab.stop();
         print("stop")
      elif key == ord('q'):#if you see the arduco
         break
curses.wrapper(main)
      
      
      

      
   
