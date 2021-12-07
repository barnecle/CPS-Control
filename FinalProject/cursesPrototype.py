#import RPi.GPIO as GPIO
#import time
<<<<<<< HEAD
from python.AlphaBot2 import AlphaBot2
=======
from AlphaBot2 import AlphaBot2
>>>>>>> 52340f3c254b573e0c7916df985593e9e9616001
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
         Ab.forward_slow();
         print("up")
      elif key == ord('a'):
         Ab.left_slow();
         print("left")
      elif key == ord('s'):
         Ab.backward_slow();
         print("backward")
      elif key == ord('d'):
         Ab.right_slow();
         print("right")
      elif key == ord(' '):
         Ab.stop();
         print("stop")
      elif key == ord('q'):#if you see the arduco
         break
curses.wrapper(main)
      
      
      

      
   
