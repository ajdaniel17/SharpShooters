from approxeng.input.selectbinder import ControllerResource
import MecanumDrive as MD
import read
from time import sleep 

leftx = 0.0
lefty = 0.0
rightx = 0.0
righty = 0.0


while True:
    try:
        with ControllerResource() as joystick:
            print('Found a controller!')
            Drive = MD.MecanumDrive(joystick.lx,joystick.ly,joystick.rx,joystick.ry)
            Drive.start()
            Vision = read.vision() 
            Vision.start()
            while joystick.connected:
                  
                presses = joystick.check_presses()

                if joystick.presses.circle:
                     Vision.display()

                if joystick.r1:
                    
                    if(Vision.foundit()):

                        Xdis = Vision.Xdist()
                        Ydis = Vision.Ydist()
                        print('Found X: ' + str(Xdis) + ' Y: ' + str(Ydis))
                        if(Xdis > 5):
                            Xmov = 100
                        elif (Xdis < -5):
                            Xmov = -100
                        else:
                            Xmov = 0

                        if(Ydis > 5):
                            Ymov = 100
                        elif (Ydis < -5):
                            Ymov = -100
                        else:
                            Ymov = 0
                        
                        Drive.update(0,0,Xmov,Ymov)
                        

                else:
                    Drive.update(joystick.lx,joystick.ly,joystick.rx,joystick.ry)
                
                
                    
            print('Connection with controller lost!')
            
    except IOError:
        print('Unable to find any joysticks')
        sleep(1.0)