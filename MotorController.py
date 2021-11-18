import RPi.GPIO as GPIO
from time import sleep
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor (threading.Thread):
    in1 = 0
    in2 = 0
    power = 0

    def __init__(self,i1,i2):
        threading.Thread.__init__(self)
        self.in1 = i1
        self.in2 = i2
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)

    def setpower(self,p):
        self.power = p

    def getpower(self):
        return self.power
  
    def run(self):
        frq = 1/60.0
        
        while (True):
            if (self.power < 0):
                if(self.power < -100):
                    self.power = -100

                #self.power = self.power * -1

                GPIO.output(self.in2,GPIO.LOW)
                GPIO.output(self.in1,GPIO.HIGH)
                sleep(abs(frq*(self.power/100.0)))
                GPIO.output(self.in1,GPIO.LOW)
                sleep(abs(frq*((100+self.power)/100.0)))

            elif (self.power > 0):
                if(self.power > 100):
                    self.power = 100
                #print(self.power/100)
                GPIO.output(self.in1,GPIO.LOW)
                GPIO.output(self.in2,GPIO.HIGH)
                sleep(abs(frq*(self.power/100.0)))
                GPIO.output(self.in2,GPIO.LOW)
                sleep(abs(frq*((100-self.power)/100.0)))
            else:
                #print("Nopower")
                GPIO.output(self.in1,GPIO.LOW)
                GPIO.output(self.in2,GPIO.LOW)
