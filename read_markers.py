#!/usr/bin/python3

import cv2

vid = cv2.VideoCapture(0)
arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters_create()
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # Display the resulting frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    frame = cv2.aruco.drawDetectedMarkers(image=frame, corners=corners, ids=ids, borderColor=(0, 255, 0))

    cv2.imshow('frame', frame)
    if ids != None:
        id1 = ids[0][0]
        c1 = corners[0][id1][0]
        c2 = corners[0][id1][1]
        c3 = corners[0][id1][2]
        c4 = corners[0][id1][3]
        print("Corners=",c1,c2,c3,c4)
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

