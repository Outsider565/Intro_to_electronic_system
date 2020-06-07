#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# start daemon first: sudo pigpiod
import pigpio
PWM = 17
pi = pigpio.pi()
print(pi.connected())
pi.set_PWM_frequency(PWM, 10)
pi.set_PWM_range(PWM, 100)
pi.set_PWM_dutycycle(PWM, 30)
