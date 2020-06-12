import RPi.GPIO as GPIO
import wiringpi

EA, I2, I1, EB, I4, I3 = (13, 19, 26, 16, 20, 21)
FREQUENCY = 200
L_COMPENSATOR = 2


class CarPower:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
        GPIO.output([EA, I1, EB, I4], GPIO.LOW)
        GPIO.output([I2, I3], GPIO.HIGH)
        self.left_power = 0
        self.right_power = 0
        self.speed = {'l': 0, 'r': 0}
        self.pwm_left = GPIO.PWM(EA, FREQUENCY)
        self.pwm_right = GPIO.PWM(EB, FREQUENCY)
        self.pwm_left.start(0)
        self.pwm_right.start(0)

    def set_left_power(self, val):
        assert -100 <= val <= 100, "left_power must be -100-100"
        if val < 0:
            GPIO.output(I1, GPIO.LOW)
            GPIO.output(I2, GPIO.HIGH)
            self.pwm_left.ChangeDutyCycle(-1 * val - L_COMPENSATOR)
        else:
            GPIO.output(I2, GPIO.LOW)
            GPIO.output(I1, GPIO.HIGH)
            self.pwm_left.ChangeDutyCycle(val - L_COMPENSATOR)
        self.left_power = val

    def set_right_power(self, val):
        assert -100 <= val <= 100, "right_power must be -100-100"
        if val < 0:
            GPIO.output(I4, GPIO.LOW)
            GPIO.output(I3, GPIO.HIGH)
            self.pwm_right.ChangeDutyCycle(-1 * val)
        else:
            GPIO.output(I3, GPIO.LOW)
            GPIO.output(I4, GPIO.HIGH)
            self.pwm_right.ChangeDutyCycle(val)
        self.right_power = val

    def set_both_power(self, val):
        self.set_left_power(val)
        self.set_right_power(val)

    def get_l_power(self):
        return self.left_power

    def get_r_power(self):
        return self.right_power

    @staticmethod
    def stay(t):
        wiringpi.delay(int(1000 * t))

    def free(self):
        self.pwm_left.stop()
        self.pwm_right.stop()
        GPIO.cleanup()

    def set_r_mode(self):
        print("warning in R mode")
        global I1, I2, I3, I4
        I1, I2 = I2, I1
        I3, I4 = I4, I3


if __name__ == '__main__':
    c = CarPower()
    c.set_left_power(30)
    # c.set_right_power(-30)
    c.stay(2)
