'''ultrasonic ranging using I2C'''
'''software tools : smbus'''
'''hardware       : KS103    '''

import smbus
import time

bus = smbus.SMBus(1) #open /dev/i2c-1
address = 0x74 #i2c device address
wr_cmd = 0xb4 #range 0-5m, return distance(mm)
#rd_cmd = 0xb2 
##range 0-5m, return flight time(us), remember divided by 2
try:
    while True:
        bus.write_byte_data(address, 0x2, wr_cmd)
        time.sleep(1) #MIN ~ 0.033
        HighByte = bus.read_byte_data(address, 0x2)
        LowByte = bus.read_byte_data(address, 0x3)
        Dist = (HighByte << 8) + LowByte
        print('Distance:', Dist/10.0, 'cm')
        #time.sleep(2)
except KeyboardInterrupt:
    pass
bus.close()
print('Range over!')
