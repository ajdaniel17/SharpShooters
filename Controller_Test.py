from approxeng.input.selectbinder import ControllerResource
import RPi.GPIO as GPIO
from time import sleep
import math

# Get a joystick
with ControllerResource(dead_zone=0.1, hot_zone = .001) as joystick:
    # print(joystick.lx.value)
    lastLY = 0
    lastLX = 0
    lastRY = 0
    lastRX = 0
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setwarnings(False)
    GPIO.setup(2,GPIO.OUT)
    GPIO.setup(3,GPIO.OUT)
    GPIO.setup(4,GPIO.OUT)
    GPIO.setup(17,GPIO.OUT)

    GPIO.output(2,GPIO.LOW)
    GPIO.output(3,GPIO.LOW)
    GPIO.output(4,GPIO.LOW)
    GPIO.output(17,GPIO.LOW)
    i = False
    # Loop until we're disconnected
    while joystick.connected:
        # This is an instance of approxeng.input.ButtonPresses
        presses = joystick.check_presses()

        
        left_y = joystick.ly
        left_x = joystick.lx
        right_y = joystick['ry']
        right_x = joystick['rx']
        
        mag = math.sqrt(pow(right_y,2)+pow(right_x,2))
        if mag > 1:
            mag = 1
        arange = (mag)
        angle = math.atan2(right_y,right_x)

        newX = math.cos(angle)
        newY = math.sin(angle)
        if(joystick.r2):
            print("yeah")
        print(joystick.r2)
       # print(newX)
        #if(lastLY != left_y):
            #print("Left Y: %.4f" % left_y)

        #if(lastLX != left_x):
            #print("Left X: %.4f" % left_x)

        #if(lastRY != right_y):
            #print("Right Y: %.4f" % right_y)

        #if(lastRX != right_x):
            #print("Right X: %.4f" % right_x)


        #print("Right Y: %.4f" % right_y)
        #print("Right X: %.4f" % right_x)
        sleep(.5)

        lastLY = left_y
        lastLX = left_x
        lastRY = right_y
        lastRX = right_x

        # while(True):
        #     joystick.rumble()
    
        if joystick.presses.circle:
            GPIO.output(2,GPIO.HIGH)
            #i = not i
        else:
            GPIO.output(2,GPIO.LOW)
            

        if joystick.presses.square:
            GPIO.output(3,GPIO.HIGH)
        else:
            GPIO.output(3,GPIO.LOW)
         
        if joystick.presses.triangle:
            GPIO.output(4,GPIO.HIGH)
        else:
            GPIO.output(4,GPIO.LOW)
         
        if joystick.presses.cross:
            GPIO.output(17,GPIO.HIGH)
        else:
            GPIO.output(17,GPIO.LOW)
         
        # if presses['square']:
        #     print('SQUARE pressed since last check')
        # # We can also use attributes directly, and get at the presses object from the controller:
        # if joystick.presses.circle:
        #     print('CIRCLE pressed since last check')
        # # Or we can use the 'x in y' syntax:
        # if 'triangle' in presses:
        #     print('TRIANGLE pressed since last check')

        # If we had any presses, print the list of pressed buttons by standard name
        if joystick.has_presses:
            print(joystick.presses)