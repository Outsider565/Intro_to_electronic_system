#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PWM = 21
FREQUENCY = 40
DUTY = 0.4
GPIO.setup(PWM, GPIO.OUT)

# don't use too large freq
def calc_delay_period(freq, duty):
    t = 1.0/freq
    ph = t*duty
    pl = t - ph
    return ph, pl

period_h, period_l = calc_delay_period(FREQUENCY, DUTY)

try:
    while True:
        GPIO.output(PWM, GPIO.HIGH)
        time.sleep(period_h)
        GPIO.output(PWM, GPIO.LOW)
        time.sleep(period_l)
except KeyboardInterrupt:
    pass
GPIO.cleanup()
