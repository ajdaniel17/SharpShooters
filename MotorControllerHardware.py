import RPi.GPIO as GPIO
#import threading
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():

    ENA = 0
    in1 = 0
    in2 = 0
    power = 0
    def __init__(self,PWM,i1,i2):
        self.ENA = PWM
        self.in1 = i1
        self.in2 = i2
        GPIO.setup(self.ENA,GPIO.OUT)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        self.pi_pwm = GPIO.PWM(self.ENA,60)
        self.pi_pwm.start(0)

    def setpower(self,p):
        pp = 0
        if p > 100:
            pp = 100
        elif p < -100:
            pp = -100
        else:
            pp = p

        self.power = pp
        self.pi_pwm.ChangeDutyCycle(abs(pp))

        if self.power > 0:
                GPIO.output(self.in1,GPIO.HIGH)
                GPIO.output(self.in2,GPIO.LOW)
        elif self.power < 0:
                GPIO.output(self.in1,GPIO.LOW)
                GPIO.output(self.in2,GPIO.HIGH)
        else:
                GPIO.output(self.in1,GPIO.LOW)
                GPIO.output(self.in2,GPIO.LOW)

        
        
    def getpower(self):
        return self.power


# m1 = Motor(12,2,3)
# #while True:
# m1.setpower(30)
# sleep(2)
# m1.setpower(75)
# sleep(2)