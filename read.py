#Make sure you have these libraries
#pip install (pyserial,numpy,opencv-contrib-python)
import cv2 #OpenCV
import numpy as np #Math
import threading
from time import sleep
import time

xtar = 320
ytar = 240

class vision_process(threading.Thread):
    go = 0
    show = 0
    cX = 0
    cY = 0
    found = 0
    def __init__(self):
        threading.Thread.__init__(self)
        
    def begin(self):
        self.go = 1
    
    def setMask(self,lm,f):
        self.light_mask = lm
        self.frame = f
        
    def getFrame(self):
        return self.frame

    def display(self,s):
        self.show = s

    def foundit(self):
        return self.found

    def posX(self):
        return self.cX

    def posY(self):
        return self.cY

    def run(self):
        while True:
            while self.go == 1:
                contours = cv2.findContours(self.light_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                contours = contours[0] if len(contours) == 2 else contours[1]
                min_area = 300
                max_area = 99000
                image_number = 0
                for con in contours:
                    area = cv2.contourArea(con)
                    if area > min_area and area < max_area:
                        x,y,w,h = cv2.boundingRect(con)
                        if h < w + 5 and h > w - 5:
                            self.found = 1
                            M = cv2.moments(con)
                            self.cX = int(M["m10"] / M["m00"])
                            self.cY = int(M["m01"] / M["m00"])
                           # print('Found Square')
                            cv2.circle(self.frame,(self.cX,self.cY),7,(0,255,255),2)
                            cv2.rectangle(self.frame,(x,y),(x+w,y+h),(255,0,0),2)
                    image_number += 1
                self.found = 0
                if(self.show == 1):
                    cv2.imshow('video',self.frame)
                    if cv2.waitKey(1)==27:# esc Key
                        break
                else:
                    cv2.destroyAllWindows()


class vision(threading.Thread):
    Xdis = 0
    Ydis = 0
    found = 0
    def __init__(self):
        threading.Thread.__init__(self)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,640)
        self.cap.set(4,480)
        self.show = 0
        self.process = vision_process()
        self.process.start()

    def display(self):
        if(self.show == 1):
            print('No longer Displaying')
            self.show = 0
            self.process.display(self.show)
        else:
            print('Now Dislaying')
            self.show = 1
            self.process.display(self.show)


    def foundit(self):
        return self.found

    def Xdist(self):
        return self.Xdis

    def Ydist(self):
        return self.Ydis

    def run(self):
        light_lower = np.array([0, 0, 250], np.uint8) 
        light_upper = np.array([5, 20,255], np.uint8)
    
        kernal = np.ones((3, 3), "uint8")
        while True:
     
            ret, frame = self.cap.read()
            cv2.circle(frame,(xtar,ytar),5,(0,0,255),2)

            #Convert frame to HSV values
            hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
            #Define Upper and lower color limits, then define the mask
            
            light_mask = cv2.inRange(hsvFrame, light_lower, light_upper)

       
            

            #redefine the light mask using the kernal and then combine the frame and the mask
            light_mask = cv2.dilate(light_mask, kernal)

            self.process.setMask(light_mask,frame)
            self.process.begin()
            
            if(self.process.foundit()):
                self.found = 1
                self.Xdis = self.process.posX() - xtar
                self.Ydis = ytar - self.process.posY()
                #print ("Xdistance is " + str(self.Xdis))
                #print ("Ydistance is " + str(self.Ydis))
            else:
                self.found = 0

            
