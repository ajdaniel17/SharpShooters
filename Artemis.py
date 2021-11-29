from approxeng.input.selectbinder import ControllerResource
import MecanumDrive as MD
import read
from time import sleep 
import time
import sys
import RPi.GPIO as GPIO
import vlc
import random

# p = vlc.MediaPlayer("I_dbyou.mp3")
q = vlc.MediaPlayer("Turret_turretsquashed04.wav")
icu1 = vlc.MediaPlayer("icu1.mp3")
tur = vlc.MediaPlayer("tur.mp3")
tur2 = vlc.MediaPlayer("tur2.mp3")
TargetA = vlc.MediaPlayer("TargetA.wav")
hi = vlc.MediaPlayer("hi.wav")
ExuseMe = vlc.MediaPlayer("ExcuseMe.wav")
Failure = vlc.MediaPlayer("Failure.wav")
Hurray = vlc.MediaPlayer("Hurray.wav")

random.seed()

on = 0

leftx = 0.0
lefty = 0.0
rightx = 0.0
righty = 0.0
prev = 0
Drive = MD.MecanumDrive(0,0,0,0)
Drive.start()
Vision = read.VisionTrack() 
Vision.start()

#mixer.init()
#sound1 = mixer.Sound("I_you.mp3")

GPIO.setup(22,GPIO.OUT)
GPIO.output(22,GPIO.LOW)

#Was going to make a class for LED Debug Stuff
GPIO.setup(9,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)

GPIO.output(9,GPIO.HIGH)
GPIO.output(10,GPIO.HIGH)
sleep(1)
GPIO.output(9,GPIO.LOW)
GPIO.output(10,GPIO.LOW)

GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.LOW)

GPIO.setup(27,GPIO.OUT)
GPIO.output(27,GPIO.LOW)

movtype = 1

DAngle = 93.5
AW = .1
Xmov = 0
Ymov = 0
movturn = 0
turn = 0

while True:
    
    try:
        with ControllerResource() as joystick:
            print('Found a controller!')
            
            while joystick.connected:
                GPIO.output(9,GPIO.LOW)
                presses = joystick.check_presses()
                if joystick.r2:
    
                    if joystick.presses.cross:
                        hi.stop()
                        hi.play()

                    if joystick.presses.square:
                        ExuseMe.stop()
                        ExuseMe.play()

                    if joystick.presses.circle:
                        Failure.stop()
                        Failure.play()

                    if joystick.presses.triangle:
                        Hurray.stop()
                        Hurray.play()

                    

                else:
                    if joystick.presses.triangle:
                        print("Exiting Code!")
                        quit()
                    
                    if joystick.presses.cross:
                        q.stop()
                        q.play()
                        print("Playing Sound")
                
                        
                        
                    if joystick.presses.select:
                        if on == 0:
                            on = 1
                            print("Turning Robot ON")
                            GPIO.output(27,GPIO.HIGH)
                        elif on == 1:
                            on = 0
                            print("Turning Robot OFF")
                            GPIO.output(27,GPIO.LOW)

                    if joystick.presses.circle:
                        Vision.display()

                    if joystick.l1:
                        GPIO.output(22,GPIO.HIGH)
                    else:
                        GPIO.output(22,GPIO.LOW)

                    if joystick.presses.dup:
                        Vision.ChangeYTar(-1)
                    if joystick.presses.ddown:
                        Vision.ChangeYTar(1)
                    if joystick.presses.dleft:
                        Vision.ChangeXTar(1)
                    if joystick.presses.dright:
                        Vision.ChangeXTar(-1)
                    
                    if joystick.presses.start:
                        Vision.resetTar()
                    
                    if joystick.presses.square:
                        if(movtype == 1):
                            #joystick.set_led(2,1)
                            print("Mode 2")
                            movtype = 2
                        elif(movtype == 2):
                            #joystick.set_led(1,1)
                            print("Mode 1")
                            movtype = 1

                    if joystick.r1:
                        
                        gen = 1
                        GPIO.output(17,GPIO.HIGH)
                        
                        Vision.Runit()
                        sleep(.05)
                        if(Vision.itgood() == 0):
                            sleep(.01)
                        elif(Vision.foundit()):

                            if (gen == 1):
                                i = random.randint(0,2)
                                

                            #if(i == 0):
                            TargetA.play()
                            # elif(i==1):
                            #     tur.play()
                            # elif(i==2):
                            #     tur2.play()

                            #print("Found")
                            Xdis = Vision.getXdis()
                            Ydis = Vision.getYdis()
                            Angle = Vision.getAngle()

                            #print('Found X: ' + str(Xdis) + ' Y: ' + str(Ydis))
                            

                            if(movtype == 1):
                                if(Xdis > 50):
                                    Xmov = .50
                                elif(Xdis < -50):
                                    Xmov = -.50
                                elif(Xdis > 5):
                                    Xmov = .30
                                elif (Xdis < -5):
                                    Xmov = -.30
                                else:
                                    Xmov = 0

                                if(Ydis > 50):
                                    Ymov = -.50
                                elif(Ydis < -50):
                                    Ymov = .50
                                elif(Ydis > 5):
                                    Ymov = -.30
                                elif (Ydis < -5):
                                    Ymov = .30
                                else:
                                    Ymov = 0

                            elif(movtype == 2):

                                if(Xdis > 50):
                                    Xmov = .70
                                elif(Xdis < -50):
                                    Xmov = -.70
                                elif(Xdis > 5):
                                    Xmov = .50
                                elif (Xdis < -5):
                                    Xmov = -.50
                                else:
                                    Xmov = 0

                                if(Ydis > 50):
                                    Ymov = -.70
                                elif(Ydis < -50):
                                    Ymov = .70
                                elif(Ydis > 5):
                                    Ymov = -.50
                                elif (Ydis < -5):
                                    Ymov = .50
                                else:
                                    Ymov = 0   

                                
                                    
                            
                            if(Xmov == 0 and Ymov == 0):
                                # print(Angle)
                                # if(Angle > (DAngle + AW) and Angle < 100):
                                #     turn = -.09
                                # elif(Angle < (DAngle - AW) and Angle > 90):
                                #     turn = .09
                                # else:
                                #     turn = 0
                                joystick.rumble()
                                gen = 0
                                
                            else:
                                turn = 0
                            Drive.update(turn,0,Xmov,Ymov)
                    
                        else:
                            #print("Not Found")
                            Drive.update(0,0,0,0)

                    else:
                        Drive.update(joystick.lx,joystick.ly,joystick.rx,joystick.ry)
                        GPIO.output(17,GPIO.LOW)
                        gen = 1
                        icu1.stop()
                        tur.stop()
                        tur2.stop()
                        TargetA.stop()
                    
                
                    
            print('Connection with controller lost!')
            Drive.update(0,0,0,0)
            GPIO.output(9,GPIO.HIGH)
    except IOError:
        print('Unable to find any joysticks')
        Drive.update(0,0,0,0)
        GPIO.output(9,GPIO.HIGH)
        sleep(1.0)