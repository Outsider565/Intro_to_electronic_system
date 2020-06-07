#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

EA, I2, I1 = (13, 19, 26)
BTN1, BTN2 = (6, 5)
FREQUENCY = 50

DUTYS = (0, 20, 40, 60, 80, 100)
duty_level = len(DUTYS) - 1

GPIO.setmode(GPIO.BCM)
GPIO.setup([EA, I2, I1], GPIO.OUT)
GPIO.output([EA, I2], GPIO.LOW)
GPIO.output(I1, GPIO.HIGH)
GPIO.setup([BTN1, BTN2], GPIO.IN, 
	pull_up_down = GPIO.PUD_UP)

pwm = GPIO.PWM(EA, FREQUENCY)
pwm.start(DUTYS[duty_level])
print("duty = %d" % DUTYS[duty_level])

def btn_pressed(btn):
    return GPIO.input(btn) == GPIO.LOW

def update_duty_level(delta):
    global duty_level
    old = duty_level
    duty_level = (duty_level + delta) % len(DUTYS)
    pwm.ChangeDutyCycle(DUTYS[duty_level])
    print("duty: %d --> %d" % (DUTYS[old], DUTYS[duty_level]))



btn1_released = True
btn2_released = True
try:
    while True:
        if btn1_released:
            if btn_pressed(BTN1):
                time.sleep(0.01)
                if btn_pressed(BTN1):
                    update_duty_level(-1)
                    btn1_released = False
        else:
            if not btn_pressed(BTN1):
                btn1_released = True
        if btn2_released:
            if btn_pressed(BTN2):
                time.sleep(0.01)
                if btn_pressed(BTN2):
                    update_duty_level(1)
                    btn2_released = False
        else:
            if not btn_pressed(BTN2):
                btn2_released = True
except KeyboardInterrupt:
    pass
pwm.stop()
GPIO.cleanup()
                