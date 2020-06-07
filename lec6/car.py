import RPi.GPIO as GPIO
import time
EA, I2, I1, EB, I4, I3 = (13, 19, 26, 16, 20, 21)  # 设置端口号
FREQUENCY = 64


class Car_Basis:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
        GPIO.output([EA, I1, EB, I4], GPIO.LOW)
        GPIO.output([I2, I3], GPIO.HIGH)
        self.left_speed = 0
        self.right_speed = 0
        self.pwm_left = GPIO.PWM(EA, FREQUENCY)
        self.pwm_right = GPIO.PWM(EB, FREQUENCY)
        self.pwm_left.start(0)
        self.pwm_right.start(0)

    def get_left_speed(self):
        return self.left_speed

    def get_right_speed(self):
        return self.right_speed

    def set_left_speed(self, val):
        assert 0 <= val <= 100
        self.pwm_left.ChangeDutyCycle(val)
        self.left_speed = val

    def set_right_speed(self, val):
        assert 0 <= val <= 100
        self.pwm_right.ChangeDutyCycle(val)
        self.right_speed = val

    def free(self):
        self.pwm_left.stop()
        self.pwm_right.stop()
        GPIO.cleanup()



class Car():
    def __init__(self):
        self.basis = Car_Basis()
        self.left_speed = 0
        self.right_speed = 0

    def done():
        self.basis.set_left_speed(self.left_speed)
        self.basis.set_right_speed(self.right_speed)

    def forward():
        self.left_speed=20
        self.right_speed=20
        self.done()

    def left_turn(t=0.5):
        self.left_speed=0.8*self.left_speed
        self.done()
        time.sleep(t)
