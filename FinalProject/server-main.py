import cv2
import struct
import redis
import numpy as np
import pickle
import os

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
    while key != 27:
        ret, img = cam.read()
		gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		corners, ids, rejected_corners = cv2.aruco.detectMarkers(gray_frame, aruco_dictionary, parameters=parameters)
		#img = cv2.aruco.drawDetectedMarkers(image=img, corners=corners, ids=ids, borderColor=(0, 255, 0))
		#img = cv2.aruco.drawDetectedMarkers(image=img, corners=rejected_corners, borderColor=(0, 0, 255))
		#cv2.imshow('frame', frame)
		if ids is not None:
        # rvecs and tvecs are the rotation and translation vectors respectively, for each of the markers in corners.
        #rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 1, cameraMatrix, distCoeffs)
			rvecs, tvecs = cv2.aruco.estimatePoseSingleMarkers(corners, .042 , cameraMatrix, distCoeffs)
			for rvec, tvec in zip(rvecs, tvecs):
            # cv2.aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, 1)
				cv2.aruco.drawAxis(img, cameraMatrix, distCoeffs, rvec, tvec, .030)

        key = cv2.waitKey(1) & 0xFF
        toRedis(r, img, 'latest',count)
        count += 1
        print(count)
		#print(tvec, rvec)
