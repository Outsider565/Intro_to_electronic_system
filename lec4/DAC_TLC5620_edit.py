# Digital to Analog
# TLC5620

# TLC5620           Pi
# CLK(7)    -----   Pin37
# DATA(6)   -----   Pin38
# LOAD(8)   -----   Pin40

# VDD(14)   -----   5V
# GND(1)    -----   GND
# LDAC(13)  -----   GND
# REFA(2)   -----   3.3V
# DACA(12)  -----   Analog Output

import RPi.GPIO as GPIO

DAC_CLK = 26  # 37
DAC_DATA = 20  # 38
DAC_LOAD = 21  # 40


def setup(clk=26, data=20, load=21):  # 37,38,40
    global DAC_CLK, DAC_DATA, DAC_LOAD
    DAC_CLK = clk
    DAC_DATA = data
    DAC_LOAD = load
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DAC_CLK, GPIO.OUT)
    GPIO.setup(DAC_DATA, GPIO.OUT)
    GPIO.setup(DAC_LOAD, GPIO.OUT)


def destroy():
    GPIO.cleanup()


def SendOneData(num, a1=0, a0=0, rng=0):
    GPIO.output(DAC_LOAD, 1)

    GPIO.output(DAC_DATA, a1)
    GPIO.output(DAC_CLK, 1)
    GPIO.output(DAC_CLK, 0)   # Output A1

    GPIO.output(DAC_DATA, a0)
    GPIO.output(DAC_CLK, 1)
    GPIO.output(DAC_CLK, 0)   # Output A0

    GPIO.output(DAC_DATA, rng)
    GPIO.output(DAC_CLK, 1)
    GPIO.output(DAC_CLK, 0)   # Output RNG

    if num > 255:
        num = 255  # 如果超出可以输出的电压最大值，默认为最大值
    i = 8
    while i > 0:
        num = num % 256  # 这里截掉了后面的位数，之前的问题应该在这里发生的
        this_bit = int(num/128)
        GPIO.output(DAC_DATA, this_bit)
        GPIO.output(DAC_CLK, 1)
        GPIO.output(DAC_CLK, 0)   # Output Di
        num = num << 1
        i = i-1

    GPIO.output(DAC_LOAD, 0)


def loop():
    while 1:
        num = int(input("input a integer(0~255):"))
        SendOneData(num)


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
