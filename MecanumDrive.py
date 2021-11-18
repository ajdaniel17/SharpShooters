import MotorControllerHardware as MC
import math
from time import sleep 
import threading



class MecanumDrive(threading.Thread):
    def __init__(self,lx,ly,rx,ry):
        threading.Thread.__init__(self)
        self.m1 = MC.Motor(12,7,8)
        #self.m1.start()
        self.m4 = MC.Motor(13,5,6)
        #self.m4.start()

        self.m3 = MC.Motor(18,14,15)
        #self.m3.start()
        self.m2 = MC.Motor(19,26,16)
        #self.m2.start()
        self.lx = lx
        self.ly = ly
        self.rx = rx
        self.ry = ry

    def update(self,lx,ly,rx,ry):
        self.lx = lx
        self.ly = ly
        self.rx = rx
        self.ry = ry

    def run(self):
        while True:
            left_y = self.ly
            left_x = self.lx
            right_y = self.ry
            right_x = self.rx

            
            right_Angle = (math.atan2(right_y,right_x)*180/math.pi+360)%360
            right_Mag = math.sqrt(pow(right_x,2)+pow(right_y,2))
            if(right_Mag > 1):
                right_Mag = 1
            sleep(0.05)
            #print(right_Mag)
            if(abs(right_x) < 0.05 and abs(right_y) <0.05):
                self.m1.setpower(0)
                self.m2.setpower(0)
                self.m3.setpower(0)
                self.m4.setpower(0)
                #print('No Angle')
            else:   
                #print(right_Angle)
                if((right_Angle >= 0.0) and (right_Angle < 90.0)):
                    self.m1.setpower(100*right_Mag)
                    self.m4.setpower(100*right_Mag)

                    m2_power = -math.cos(2*right_Angle*math.pi/180)*100
                    m3_power = -math.cos(2*right_Angle*math.pi/180)*100

                    self.m2.setpower(m2_power*right_Mag)
                    self.m3.setpower(m3_power*right_Mag)
                if((right_Angle >= 90.0) and (right_Angle < 180.0)):
                    self.m2.setpower(100*right_Mag)
                    self.m3.setpower(100*right_Mag)

                    m1_power = -math.cos(2*right_Angle*math.pi/180)*100
                    m4_power = -math.cos(2*right_Angle*math.pi/180)*100

                    self.m1.setpower(m1_power*right_Mag)
                    self.m4.setpower(m4_power*right_Mag)
                if((right_Angle >= 180.0) and (right_Angle < 270.0)):
                    self.m1.setpower(-100*right_Mag)
                    self.m4.setpower(-100*right_Mag)

                    m2_power = math.cos(2*right_Angle*math.pi/180)*100
                    m3_power = math.cos(2*right_Angle*math.pi/180)*100

                    self.m2.setpower(m2_power*right_Mag)
                    self.m3.setpower(m3_power*right_Mag)
                if((right_Angle >= 270.0) and (right_Angle < 360.0)):
                    self.m2.setpower(-100*right_Mag)
                    self.m3.setpower(-100*right_Mag)

                    m1_power = math.cos(2*right_Angle*math.pi/180)*100
                    m4_power = math.cos(2*right_Angle*math.pi/180)*100

                    self.m1.setpower(m1_power*right_Mag)
                    self.m4.setpower(m4_power*right_Mag)

            if(left_x < -.05):
                self.m1.setpower(self.m1.getpower()+(left_x*100))
                self.m2.setpower(self.m2.getpower()-(left_x*100))
                self.m3.setpower(self.m3.getpower()+(left_x*100))
                self.m4.setpower(self.m4.getpower()-(left_x*100))
            elif(left_x > .05):
                self.m1.setpower(self.m1.getpower()+(left_x*100))
                self.m2.setpower(self.m2.getpower()-(left_x*100))
                self.m3.setpower(self.m3.getpower()+(left_x*100))
                self.m4.setpower(self.m4.getpower()-(left_x*100))





