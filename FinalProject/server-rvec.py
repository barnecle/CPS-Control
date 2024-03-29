import cv2
import struct
import redis
import numpy as np
import pickle
import os
import time

from Alphabot2 import AlphaBot2
import curses


Ab = AlphaBot2()

def main(stdscr):
   Ab.setPWMA(10)
   Ab.setPWMB(10)
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
      elif key == ord('q'): #if you see the arduco
         break
      elif key == ord('x'): # exit the program
         exit()
#curses.wrapper(main)

def toRedis(r,a,n,fnum):
   h, w = a.shape[:2]             # Shape of the h, w and not the 3 colors in the depth of the image
   shape = struct.pack('>II',h,w) # Pack the height and the width variables into variable shape
                                  # Big Endian  
   encoded = shape + a.tobytes()  # concatenate the shape variable and the encoded image
   r.hmset(n,{'frame':fnum,'image':encoded})
   return

if __name__ == '__main__':
   if not os.path.exists('calibration.pckl'):
      print("You need to calibrate the camera you'll be using. See calibration script.")
      exit()
   else:
      f = open('calibration.pckl', 'rb')
      cameraMatrix, distCoeffs = pickle.load(f)
      f.close()
      if cameraMatrix is None or distCoeffs is None:
         print("Calibration issue. Remove ./calibration.pckl and recalibrate your camera")
         exit()
   aruco_dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
   parameters = cv2.aruco.DetectorParameters_create()
   r = redis.Redis('140.182.152.14', port=6379, db=0)
   cam = cv2.VideoCapture(0)
   cam.set(3, 320)
   cam.set(4, 240)
   key = 0
   count = 0
   target_distance = 0.3
   error_x = 0
   error_z = 0
   error_r = 0
   last_error_x = error_x
   last_error_z = error_z
   last_error_r = error_r
   Px_coef = 75
   Ix_coef = 0
   Dx_coef = 30

   Pr_coef = 50
   Ir_coef = 0
   Dr_coef = 10
   
   Pz_coef = 1/2
   Iz_coef = 0
   Dz_coef = 0
   integral_x = 0 
   integral_z = 0
   integral_r = 0

   maximum_speed = 20
   speed = 0
   
   
   while(True):
      curses.wrapper(main)
      
      Ab.forward() 
      while key != 27:
         start_code_time = time.time()
         ret, img = cam.read()
         if not ret:
            break
        
         gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
         corners, ids, rejected_corners = cv2.aruco.detectMarkers(gray_frame, aruco_dictionary, parameters=parameters)
   		#img = cv2.aruco.drawDetectedMarkers(image=img, corners=corners, ids=ids, borderColor=(0, 255, 0))
   		#img = cv2.aruco.drawDetectedMarkers(image=img, corners=rejected_corners, borderColor=(0, 0, 255))
   		#cv2.imshow('frame', frame)
         if ids is not None:
             rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(corners, .042 , cameraMatrix, distCoeffs)
             for rvec, tvec in zip(rvecs, tvecs):
                 cv2.aruco.drawAxis(img, cameraMatrix, distCoeffs, rvec, tvec, .030)
             key = cv2.waitKey(1) & 0xFF
             toRedis(r, img, 'latest',count)
             count += 1
             print(count)
             error_x = tvecs[0][0][0] #+ rvecs[0][0][2])/2
             error_r = rvecs[0][0][2]
             error_z = tvecs[0][0][2] - target_distance
         
   #      derivative_r = error_r - last_error_r
         derivative_x = error_x - last_error_x
   #      integral_r += error_r
         integral_x += error_x
        
         derivative_z = error_z - last_error_z
         integral_z += error_z
         power_difference = error_x*Px_coef + integral_x*Ix_coef + derivative_x*Dx_coef
    #     pid_r = error_r*Pr_coef+integral_r*Ir_coef + derivative_r*Dr_coef  
         d_speed = error_z*Pz_coef + integral_z*Iz_coef + derivative_z*Dz_coef
         
     #    power_difference = (power_difference + pid_r)/2
         speed += d_speed
         print("speed ", speed)
            #print("rvec ", rvec)
         print("x error ", error_x)
         print("pwr diff ", power_difference)         

         if (speed > maximum_speed):
             speed = maximum_speed
         if (speed < 0):
             speed = 0
         
         if power_difference > speed:
             power_difference = speed
         if power_difference < -speed:
             power_difference = -speed
         if power_difference < 0:
             Ab.setPWMA(speed + power_difference)
             Ab.setPWMB(speed)
         else:
             Ab.setPWMA(speed)
             Ab.setPWMB(speed - power_difference)
         
         last_error_x = error_x
         last_error_z = error_z
         last_error_r = error_r
            
         code_time = time.time() - start_code_time
         print("time " + str(code_time))
        # time.sleep(0.008-code_time)
