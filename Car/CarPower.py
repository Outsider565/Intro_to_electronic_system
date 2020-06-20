import RPi.GPIO as GPIO
import wiringpi

import Carlog

logger = Carlog.logger
EA, I2, I1, EB, I4, I3 = (16, 19, 26, 13, 21, 20)
FREQUENCY = 100  # PWM的调节频率
# COMPENSATOR是历史遗留代码，在新的调节过程中设置为0就行；
# 原意是通过左(右)的power=设置值-COMPENSATOR，以期达到两侧速度相同的效果；
# 但后来使用了PID进行自动闭环调节，因此此处可简单设为0
L_COMPENSATOR = 0
R_COMPENSATOR = 0


class CarPower:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([EA, I2, I1, EB, I4, I3], GPIO.OUT)
        GPIO.output([EA, I2, EB, I3], GPIO.LOW)
        GPIO.output([I1, I4], GPIO.HIGH)
        self.left_power = 0
        self.right_power = 0
        self.speed = {'l': 0, 'r': 0}
        self.pwm_left = GPIO.PWM(EA, FREQUENCY)
        self.pwm_right = GPIO.PWM(EB, FREQUENCY)
        self.pwm_left.start(0)
        self.pwm_right.start(0)

    def set_left_power(self, val):
        """
        :param val: (-100,100)之间的实数，设置左侧电机的PWM值
        """
        assert -100 <= val <= 100, "left_power must be -100-100"
        if val < 0:
            GPIO.output(I2, GPIO.LOW)
            GPIO.output(I1, GPIO.HIGH)
            self.pwm_left.ChangeDutyCycle(max(-1 * val - L_COMPENSATOR, 0))
        else:
            GPIO.output(I2, GPIO.LOW)
            GPIO.output(I1, GPIO.HIGH)
            self.pwm_left.ChangeDutyCycle(max(val - L_COMPENSATOR, 0))
        self.left_power = val

    def set_right_power(self, val):
        """
        :param val: (-100,100)之间的实数，设置右侧电机的PWM值
        """
        assert -100 <= val <= 100, "right_power must be -100-100"
        if val < 0:
            GPIO.output(I4, GPIO.LOW)
            GPIO.output(I3, GPIO.HIGH)
            self.pwm_right.ChangeDutyCycle(max(-1 * val - R_COMPENSATOR, 0))
        else:
            GPIO.output(I3, GPIO.LOW)
            GPIO.output(I4, GPIO.HIGH)
            self.pwm_right.ChangeDutyCycle(max(val - R_COMPENSATOR, 0))
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

    @staticmethod
    def set_r_mode():
        logger.warning("warning in R mode")
        global I1, I2, I3, I4
        I1, I2 = I2, I1
        I3, I4 = I4, I3


if __name__ == '__main__':
    c = CarPower()
    c.set_left_power(100)
    c.set_right_power(100)
    c.stay(5)
    c.free()
