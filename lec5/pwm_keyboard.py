#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import sys
import tty
import termios


def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)


EA, I2, I1, EB, I4, I3 = (13, 19, 26, 16, 20, 21)
FREQUENCY = 60
A_LOW_SPEED = 20
B_LOW_SPEED = 24.5
A_HIGH_SPEED = 55
B_HIGH_SPPED = 60
DUTYS_A = [{'w': A_LOW_SPEED, 'd': 0, 's': 0, 'a': A_LOW_SPEED},
    {'w': A_HIGH_SPEED, 'd': 0, 's': 0, 'a': A_HIGH_SPEED}]  # 右侧
DUTYS_B = [{'w': B_LOW_SPEED, 'd': B_LOW_SPEED, 's': 0, 'a': 0}, {'w': B_HIGH_SPPED, 'd': B_HIGH_SPPED, 's': 0, 'a': 0}]  # 左侧
EXPRESSIONS = {'w': 'move forward!',
               'd': 'turn left!',
               's': 'stop!',
               'a': 'turn right!'}

GPIO.setmode(GPIO.BCM)
GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
GPIO.output([EA, I2, EB, I3], GPIO.LOW)
GPIO.output([I1, I4], GPIO.HIGH)
r_mod=0
pwma = GPIO.PWM(EA, FREQUENCY)
pwmb = GPIO.PWM(EB, FREQUENCY)
pwma.start(DUTYS_A[0]['s'])
pwmb.start(DUTYS_B[0]['s'])
print("ready!")

while True:
    try:
        cmd = readkey()
        speed_mode= 0# 低速档
        print(cmd)
        if cmd=='r':
            if(r_mod==0):
                print("In reversed mode")
                GPIO.output([EA, I1, EB, I4], GPIO.LOW)
                GPIO.output([I2, I3], GPIO.HIGH)
                r_mod=1
            else:
                print("In normal mode")
                GPIO.output([EA, I2, EB, I3], GPIO.LOW)
                GPIO.output([I1, I4], GPIO.HIGH)
                r_mod=0
        if cmd == 'q' or ord(cmd) == 0x03:
            pwma.stop()
            pwmb.stop()
            GPIO.cleanup()
            break
        if cmd == 'h':
            print("High speed")
            speed_mode= 1
        elif cmd == 'l':
            print("Low speed")
            speed_mode= 0
        if (cmd == 'w') or (cmd == 'a') or (cmd == 's') or (cmd == 'd'):
            pwma.ChangeDutyCycle(DUTYS_A[speed_mode][cmd])
            pwmb.ChangeDutyCycle(DUTYS_B[speed_mode][cmd])
            print(EXPRESSIONS[cmd])
        else:
            pass
    except KeyboardInterrupt:
        pwma.stop()
        pwmb.stop()
        GPIO.cleanup()
