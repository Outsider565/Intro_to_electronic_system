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
B_LOW_SPEED = 23
A_HIGH_SPEED = 100
B_HIGH_SPPED = 100
DUTYS_A = {'w': A_LOW_SPEED, 'd': 0, 's': 0, 'a': A_LOW_SPEED}  # 右侧
DUTYS_B = {'w': B_LOW_SPEED, 'd': B_LOW_SPEED, 's': 0, 'a': 0}  # 左侧
EXPRESSIONS = {'w': 'move forward!',
               'd': 'turn left!',
               's': 'stop!',
               'a': 'turn right!'}

GPIO.setmode(GPIO.BCM)
GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
GPIO.output([EA, I1, EB, I4], GPIO.LOW)
GPIO.output([I2, I3], GPIO.HIGH)
r_mod = 1
pwma = GPIO.PWM(EA, FREQUENCY)
pwmb = GPIO.PWM(EB, FREQUENCY)
pwma.start(DUTYS_A['s'])
pwmb.start(DUTYS_B['s'])
print("ready!")
prev_cmd='s'
cmd='s'
while True:
    try:

        cmd = readkey()
        print(cmd)
        if cmd == 'r':
            if(r_mod == 0):
                print("In reversed mode")
                GPIO.output([I1, I4], GPIO.LOW)
                GPIO.output([I2, I3], GPIO.HIGH)
                r_mod = 1
            else:
                print("In normal mode")
                GPIO.output([I2, I3], GPIO.LOW)
                GPIO.output([I1, I4], GPIO.HIGH)
                r_mod = 0
            prev_cmd='s'
        elif cmd == 'q' or ord(cmd) == 0x03:
            pwma.stop()
            pwmb.stop()
            GPIO.cleanup()
            break
        elif cmd == 'j':
            if(DUTYS_A['w'] == 0):
                DUTYS_A['w'] =A_LOW_SPEED
                DUTYS_B['w'] =B_LOW_SPEED
            elif(DUTYS_A['w'] <= 60):
                DUTYS_A['w'] += 20
                DUTYS_B['w'] += 20
            else:
                DUTYS_A['w'] = 100
                DUTYS_B['w'] = 100
            pwma.ChangeDutyCycle(DUTYS_A[prev_cmd])
            pwmb.ChangeDutyCycle(DUTYS_B[prev_cmd])
            print("Speed: ", DUTYS_A['w'], DUTYS_B['w'])
        elif cmd == 'k':
            if(DUTYS_A['w'] > 20):
                DUTYS_A['w'] -= 20
                DUTYS_B['w'] -= 20
            else:
                DUTYS_A['w'] = 0
                DUTYS_B['w'] = 0
                
            pwma.ChangeDutyCycle(DUTYS_A[prev_cmd])
            pwmb.ChangeDutyCycle(DUTYS_B[prev_cmd])
            print("Speed: ", DUTYS_A['w'], DUTYS_B['w'])
        elif (cmd == 'w') or (cmd == 'a') or (cmd == 's') or (cmd == 'd'):
            pwma.ChangeDutyCycle(DUTYS_A[cmd])
            pwmb.ChangeDutyCycle(DUTYS_B[cmd])
            print(EXPRESSIONS[cmd])
            prev_cmd=cmd
        else:
            pass
    except KeyboardInterrupt:
        pwma.stop()
        pwmb.stop()
        GPIO.cleanup()
