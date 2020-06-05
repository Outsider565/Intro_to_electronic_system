#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# start daemon first: sudo pigpiod
import pigpio
PWM = 21
pi = pigpio.pi()
pi.set_PWM_frequency(PWM, 8000)
pi.set_PWM_range(PWM, 100)
pi.set_PWM_dutycycle(PWM, 30)