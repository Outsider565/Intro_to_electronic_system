import RPi.GPIO as GPIO
import time


def switch(channel):
    print("button pressed")
    global ledStatus
    if ledStatus == False:
        GPIO.output(led, GPIO.HIGH)
    else:
        GPIO.output(led, GPIO.LOW)


GPIO.setmode(GPIO.BCM)
led = 21
bt = 20
GPIO.setup(led, GPIO.OUT)
GPIO.setup(bt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
ledStatus = False  # 最开始都出于低电平状态，LED为关闭

GPIO.add_event_detect(bt,GPIO.FALLING,callback=switch,bouncetime=200)
try:
    while True:
        print("I love raspi")
except KeyboardInterrupt:
    pass
GPIO.cleanup()
# 这段代码有时候会出现按一次闪烁两次的情况，因为存在电路的抖动