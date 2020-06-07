import RPi.GPIO as GPIO
import time
import threading
import numpy
import matplotlib.pyplot as plt

EA, I2, I1, EB, I4, I3, LS, RS = (13, 19, 26, 16, 20, 21, 6, 12)
FREQUENCY = 50
GPIO.setmode(GPIO.BCM)
GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
GPIO.setup([LS, RS],GPIO.IN)
GPIO.output([EA, I2, EB, I3], GPIO.LOW)
GPIO.output([I1, I4], GPIO.HIGH)

pwma = GPIO.PWM(EA, FREQUENCY)
pwmb = GPIO.PWM(EB, FREQUENCY)
pwma.start(0)
pwmb.start(0)

lspeed = 0
rspeed = 0
lcounter = 0
rcounter = 0

def my_callback(channel):
        global lcounter
        global rcounter
        if (channel==LS):
            lcounter+=1
        elif(channel==RS):
            rcounter+=1
            
def getspeed():
    global rspeed
    global lspeed
    global lcounter
    global rcounter
    GPIO.add_event_detect(LS,GPIO.RISING,callback=my_callback)
    GPIO.add_event_detect(RS,GPIO.RISING,callback=my_callback)
    while True:
        rspeed=(rcounter/10.0)
        lspeed=(lcounter/10.0)
        rcounter = 0
        lcounter = 0
        time.sleep(1)
        
thread1=threading.Thread(target=getspeed)
thread1.start()

i=0
x=[]
y1=[]
y2=[]
while i<=20:
    x.append(5*i)
    pwma.ChangeDutyCycle(5*i)
    pwmb.ChangeDutyCycle(5*i)
    time.sleep(3)
    y1.append(lspeed)
    y2.append(rspeed)
    i=i+1
    		
#plt.plot(x,y1,'-o')
#plt.plot(x,y2,'-*')
print(x,y1)
print(x,y2)
pwma.stop()
pwmb.stop()
GPIO.cleanup()
#plt.show()
