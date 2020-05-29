'''ultrasonic ranging using I2C'''
'''software tools : wiringpi'''
'''hardware       : KS103    '''

import wiringpi as wpi

address = 0x74 #i2c device address
h = wpi.wiringPiI2CSetup(address) #open device at address
wr_cmd = 0xb0  #range 0-5m, return distance(mm)
#rd_cmd = 0xb2 
##range 0-5m, return flight time(us), remember divided by 2
try:
    while True:
        wpi.wiringPiI2CWriteReg8(h, 0x2, wr_cmd)
        wpi.delay(1000) #unit:ms  MIN ~ 33
        HighByte = wpi.wiringPiI2CReadReg8(h, 0x2)
        LowByte = wpi.wiringPiI2CReadReg8(h, 0x3)
        Dist = (HighByte << 8) + LowByte
        print('Distance:', Dist/10.0, 'cm')
except KeyboardInterrupt:
    pass
print('Range over!')
