import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
led = 21
bt = 20
GPIO.setup(led, GPIO.OUT)
GPIO.setup(bt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
ledStatus = False
n = 1
try:
    while True:
        time.sleep(0.01)
        if(GPIO.input(bt) == GPIO.LOW):
            time.sleep(0.03)
            if(GPIO.input(bt) == GPIO.HIGH):
                print("button pressed", n)
                n += 1
                if ledStatus == False:  # 1为开，0为关
                    GPIO.output(led, GPIO.HIGH)
                else:
                    GPIO.output(led, GPIO.LOW)
except KeyboardInterrupt:
    pass
GPIO.cleanup()
