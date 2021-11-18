#Make sure you have these libraries
#pip install (pyserial,numpy,opencv-contrib-python)
import cv2 #OpenCV
import numpy as np #Math
import threading
from time import sleep
import time



class Camera(threading.Thread):
 
    def __init__(self,w,h):
        threading.Thread.__init__(self)
        self.cap = cv2.VideoCapture(0)
        self.width = w
        self.height = h
        self.cap.set(3,self.width)
        self.cap.set(4,self.height)
        self.frame = np.zeros((100,100,3), dtype=np.uint8)

    def begin(self):
        self.go = 1

    def GetFrame(self):
        return self.frame
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def run(self):
        while True:
            ret, self.frame = self.cap.read()


class VisionTrack(threading.Thread):
    go = 0
    show = 0
    cX = 0
    cY = 0
    found = 0
    xtar = 309
    ytar = 327
    readyy = 0
    cutoff = 250
    def __init__(self):
        threading.Thread.__init__(self)
        self.cam = Camera(720,720)
        self.cam.start()
        self.xdefault = self.xtar
        self.ydefault = self.ytar
        
    def Runit(self):
        self.go = 1

    def display(self):
        if(self.show == 1):
            print('No longer Displaying')
            self.show = 0
        else:
            print('Now Dislaying')
            self.show = 1

    def foundit(self):
        return self.found

    def getXdis(self):
        return self.Xdis

    def getYdis(self):
        return self.Ydis

    def getAngle(self):
        return self.ang

    def ChangeYTar(self,num):
        self.ytar = self.ytar + num

    def ChangeXTar(self,num):
        self.xtar = self.xtar + num

    def resetTar(self):
        self.ytar = self.ydefault
        self.xtar = self.xdefault

    def itgood(self):
        return self.readyy

    def run(self):

        light_lower = np.array([0, 0, 250], np.uint8) 
        light_upper = np.array([5, 20,255], np.uint8)
    
        kernal = np.ones((3, 3), "uint8")

        min_area = 2500
        max_area = 99000


        while True:
            frame = self.cam.GetFrame()
            

            #Fuck Dre
            
            #Convert frame to HSV values
            hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            #Define Upper and lower color limits, then define the mask
            light_mask = cv2.inRange(hsvFrame, light_lower, light_upper)

            #redefine the light mask using the kernal and then combine the frame and the mask
            light_mask = cv2.dilate(light_mask, kernal)
            contours = cv2.findContours(light_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]

            res_light = cv2.bitwise_and(frame, frame, mask = light_mask)
            while self.go == 1:
                self.readyy = 0
                good = 0
                image_number = 0
                for con in contours:
                    area = cv2.contourArea(con)
                    if area > min_area:
                        #print(area)
                        x,y,w,h = cv2.boundingRect(con)
                        (x2,y2),(w2,h2),self.ang = cv2.minAreaRect(con)
                        if h < w + 20 and h > w - 20:
                            M = cv2.moments(con)
                            self.cX = int(M["m10"] / M["m00"])
                            self.cY = int(M["m01"] / M["m00"])
                            #print(self.cY)
                            #print(self.cX)
                            if(self.cY > self.cutoff ):
                                if(w > h):
                                    self.ang = self.ang+180
                                else:
                                    self.ang = self.ang+90
                                good = 1
                                print('Target X: ' + str(self.xtar) + ' Y: ' + str(self.ytar))
                                #print(self.ang)
                                self.Xdis = self.cX - self.xtar
                                self.Ydis = self.ytar - self.cY

                                cv2.circle(frame,(self.cX,self.cY),7,(0,255,255),2)
                                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                                self.readyy = 1
                    
                            
                        
                            
                            # print('Found Square')
                            
                            #cv2.rectangle(self.frame,(self.xtar+200,self.ytar-200),(self.xtar-200,self.ytar+200),(0,255,0),2)
                    else:
                        
                        self.readyy = 1
                    image_number += 1
                if(good):
                    self.found = 1
                else:
                    self.found = 0
                self.go = 0
                
                
        
            cv2.circle(frame,(self.xtar,self.ytar),5,(0,0,255),2)
            cv2.line(frame,(0,self.cutoff),(720,self.cutoff),(0,255,0),2)
            if(self.show == 1):
                cv2.imshow('video',frame)
                #cv2.imshow('video',np.hstack([frame,res_light]))
                if cv2.waitKey(1)==27:# esc Key
                    break
            else:
                cv2.destroyAllWindows()




            
            

            
