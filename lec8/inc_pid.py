#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

class SpeedMeter(object):
    def __init__(self, LS, RS, window_s = 1.0):
        self.__r_rec = []
        self.__l_rec = []
        self.__ls = LS
        self.__rs = RS
        self.__window = window_s

    def start(self):
        GPIO.add_event_detect(self.__ls, GPIO.RISING, callback = self.__cb_handler)
        GPIO.add_event_detect(self.__rs, GPIO.RISING, callback = self.__cb_handler)
        time.sleep(self.__window)

    def stop(self):
        GPIO.remove_event_detect(self.__ls)
        GPIO.remove_event_detect(self.__rs)

    def __cb_handler(self, channel):
        t = time.time()
        if channel == self.__ls:
            self.__l_rec.append(t)
            while (t - self.__l_rec[0] > self.__window):
                self.__l_rec.pop(0)
                if len(self.__l_rec) == 0:
                    break
        else:
            self.__r_rec.append(t)
            while (t - self.__r_rec[0] > self.__window):
                self.__r_rec.pop(0)
                if len(self.__r_rec) == 0:
                    break

    def get_l_speed(self):
        return len(self.__l_rec) / 20 / self.__window
    
    def get_r_speed(self):
        return len(self.__r_rec) / 20 / self.__window

#   e(k) = target - feedback(k)
#   U(k) = Kp*e(k) + Ki*Integral(0, k, e(k)) + kd*(e(k)-e(k-1))
#   delta_U(k) = U(k) - U(k-1)
#			   = Kp*(e(k)-e(k-1)) + Ki*e(k) + Kd*(e(k)-2*e(k-1)+e(k-2))
class PID(object):
    def __init__(self, pid_params, target, init_u, u_range):
        self.__Kp = pid_params[0]
        self.__Ki = pid_params[1]
        self.__Kd = pid_params[2]
        self.__target = target
        self.__u = init_u
        self.__u_min = u_range[0]
        self.__u_max = u_range[1]

        self.__e = self.__target
        self.__e_1 = self.__target
        self.__e_2 = self.__target

    def update(self, feedback):
        self.__e_2 = self.__e_1
        self.__e_1 = self.__e
        self.__e = self.__target - feedback
        du = self.__Kp*(self.__e-self.__e_1)+self.__Ki*self.__e+self.__Kd*(self.__e-2*self.__e_1+self.__e_2)
        self.__u += du
        if self.__u > self.__u_max:
            self.__u = self.__u_max
        if self.__u < self.__u_min:
            self.__u = self.__u_min
        return self.__u

# Configurations
EA, I2, I1, EB, I4, I3, LS, RS = (13, 19, 26, 16, 20, 21, 6, 12)
FREQUENCY = 50
EXPECTED_SPEED = 3.5
INIT_DUTY_L = 37
PID_PARAMS_L = (4, 2.8, 1.3)
INIT_DUTY_R = 33
PID_PARAMS_R = (4, 3.2, 1.2)
GPIO.setmode(GPIO.BCM)
GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
GPIO.setup([LS, RS],GPIO.IN)
GPIO.output([EA, I1, EB, I4], GPIO.LOW)
GPIO.output([I2, I3], GPIO.HIGH)

# Set up
pwm_l = GPIO.PWM(EA, FREQUENCY)
pwm_r = GPIO.PWM(EB, FREQUENCY)
meter = SpeedMeter(LS, RS, 1.0)
meter.start()
pid_l = PID(PID_PARAMS_L, EXPECTED_SPEED, INIT_DUTY_L, (0, 100))
pid_r = PID(PID_PARAMS_R, EXPECTED_SPEED, INIT_DUTY_R, (0, 100))
ts = [0.0]
speed_ls = [0.0]
speed_rs = [0.0]

# Start
t0 = time.time()
pwm_l.start(INIT_DUTY_L)
pwm_r.start(INIT_DUTY_R)
try:
    while True:
        speed_l = meter.get_l_speed()
        pwm_l.ChangeDutyCycle(pid_l.update(speed_l))
        speed_r = meter.get_r_speed()
        pwm_r.ChangeDutyCycle(pid_r.update(speed_r))
        ts.append(time.time() - t0)
        speed_ls.append(speed_l)
        speed_rs.append(speed_r)
        time.sleep(0.49)
except KeyboardInterrupt:    
    pwm_l.stop()
    pwm_r.stop()
    meter.stop()
    GPIO.cleanup()

plt.plot(ts, speed_ls, '-o')
plt.plot(ts, speed_rs, '-*')
plt.plot(ts, list([EXPECTED_SPEED for t in ts]), '-')
plt.show()
