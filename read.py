#Make sure you have these libraries
#pip install (pyserial,numpy,opencv-contrib-python)
import cv2 #OpenCV
import numpy as np #Math
import sys
import serial,time #Needed to communicate with Arduino

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    #Convert frame to HSV values
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  
    #Define Upper and lower color limits, then define the mask
    orange_lower = np.array([9, 50,50 ], np.uint8) #Note: I had to experiment to try and get the upper and lower limits of orange, I used https://pinetools.com/image-color-picker
    orange_upper = np.array([50, 255, 255], np.uint8)
    orange_mask = cv2.inRange(hsvFrame, orange_lower, orange_upper)

    #I have no idea what this is for
    kernal = np.ones((5, 5), "uint8")

    #redefine the orange mask using the kernal and then combine the frame and the mask
    orange_mask = cv2.dilate(orange_mask, kernal)
    res_orange = cv2.bitwise_and(frame, frame, mask = orange_mask)

    #split up the values of the HSV masks, V is in greyscale
    h, s, v1 = cv2.split(res_orange)

    #gray = cv2.medianBlur(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY),5)
    #Use v1, which only shows orange colors and is in greyscale to find circles
    circles=cv2.HoughCircles(v1, cv2.HOUGH_GRADIENT, 1.5, 50)
    if circles is not None:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")      
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(frame, center, 1, (0, 0, 255), 3)
            # circle outline
            radius = i[2]
            cv2.circle(frame, center, radius, (0, 255, 0), 3)
    else:
        print("No Circle!")
    cv2.imshow('video',np.hstack([frame,res_orange]))
    if cv2.waitKey(1)==27:# esc Key
        break
cap.release()
cv2.destroyAllWindows()