import RPi.GPIO as GPIO
import time
import wiringpi
import threading
EA, I2, I1, EB, I4, I3, LS, RS = (13, 19, 26, 16, 20, 21, 6, 12)
FREQUENCY = 50


class Car_Basis:
    l_counter = 0
    r_counter = 0

    def __init__(self, log=True):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
        GPIO.setup([LS, RS], GPIO.IN)
        GPIO.output([EA, I1, EB, I4], GPIO.LOW)
        GPIO.output([I2, I3], GPIO.HIGH)
        self.left_power = 0
        self.right_power = 0
        self.speed = {'l': 0, 'r': 0}
        self.pwm_left = GPIO.PWM(EA, FREQUENCY)
        self.pwm_right = GPIO.PWM(EB, FREQUENCY)
        self.pwm_left.start(0)
        self.pwm_right.start(0)

    @staticmethod
    def change_counter(channel):
        if (channel == LS):
            Car_Basis.lcounter += 1
        elif(channel == RS):
            Car_Basis.rcounter += 1

    @staticmethod
    def update_speed(flag,period):
        Car_Basis.l_counter = 0
        Car_Basis.r_counter = 0
        GPIO.add_event_detect(
            LS, GPIO.RISING, callback=Car_Basis.change_counter)
        GPIO.add_event_detect(
            RS, GPIO.RISING, callback=Car_Basis.change_counter)
        while not flag.isSet():
            Car_Basis.speed_dict['l'] = Car_Basis.l_counter/period
            Car_Basis.speed_dict['r'] = Car_Basis.r_counter/period
            Car_Basis.l_counter = 0
            Car_Basis.r_counter = 0
            wiringpi.delay(period)
        
    def get_speed(self,period=100):
        flag=threading.Event()
        speed_updater=threading.Thread(target=Car_Basis.update_speed,args=(flag,))

    def set_left_power(self, val):
        assert 0 <= val <= 100
        self.pwm_left.ChangeDutyCycle(val)
        self.left_power = val

    def set_right_power(self, val):
        assert 0 <= val <= 100
        self.pwm_right.ChangeDutyCycle(val)
        self.right_power = val

    @staticmethod
    def stay(t):
        """
        t的单位为ms
        """
        wiringpi.delay(t)

    def free(self):
        self.pwm_left.stop()
        self.pwm_right.stop()
        GPIO.cleanup()


class Car():
    def __init__(self):
        self.basis = Car_Basis()
        self.left_speed = 0
        self.right_speed = 0

    def done(self):
        self.basis.set_left_speed(self.left_speed)
        self.basis.set_right_speed(self.right_speed)

    def forward(self):
        self.left_speed = 20
        self.right_speed = 20
        self.done()

    def left_turn(self, t=0.5, bias=20):
        self.left_speed = ratio*self.left_speed
        self.done()
        time.sleep(t)
        self.left_speed = self.right_speed
        self.done()

    def right_turn(self, t=0.5, ratio=0.8):
        self.right_speed = ratio*self.right_speed
        self.done()
        time.sleep(t)
        self.right_speed = self.left_speed
        self.done()

    def free(self):
        self.basis.free()


if __name__ == "__main__":
    c = Car_Basis()
    c.set_left_power(100)
    c.set_right_power(100)
    c.stay(200)
    c.free()
