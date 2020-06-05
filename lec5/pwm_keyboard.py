#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

EA, I2, I1, EB, I4, I3 = (13, 19, 26, 16, 20, 21)
FREQUENCY = 50
DUTYS_A = {'w':20,'a':0, 's':0, 'd':20}
DUTYS_B = {'w':20,'a':20,'s':0, 'd':0 }
EXPRESSIONS = {'w':'move forward!',
               'a':'turn left!',
               's':'stop!',
               'd':'turn right!'}

GPIO.setmode(GPIO.BCM)
GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
GPIO.output([EA, I2, EB, I3], GPIO.LOW)
GPIO.output([I1, I4], GPIO.HIGH)

pwma = GPIO.PWM(EA, FREQUENCY)
pwmb = GPIO.PWM(EB, FREQUENCY)
pwma.start(DUTYS_A['s'])
pwmb.start(DUTYS_B['s'])
print("ready!")

while True:
    cmd = input("command >> ")
    if cmd == 'q':
        pwma.stop()
        pwmb.stop()
        GPIO.cleanup()
        break
    elif (cmd=='w') or (cmd=='a') or (cmd=='s') or (cmd=='d'):
        pwma.ChangeDutyCycle(DUTYS_A[cmd])
        pwmb.ChangeDutyCycle(DUTYS_B[cmd])
        print(EXPRESSIONS[cmd])
    else:
        pass
