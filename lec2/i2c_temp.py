'''tempature measure using I2C'''
'''software tools : smbus'''
'''hardware       : KS103    '''

import smbus
import time
import sys

bus = smbus.SMBus(1) #open /dev/i2c-1
address = 0x74 #i2c device address
wr_cmd = [0xc9, 0xca, 0xcb, 0xcc]  #tempature measurement cmd
precision = [0.5, 0.25, 0.125, 0.0625] # tempature measurement precision 
#rd_cmd = 0xb2 
##range 0-5m, return flight time(us), remember divided by 2
try:
    print('Please input number 0~3 to select tempature measurement precision. ')
    print('0 : 0.5℃,')
    print('1 : 0.25℃,')
    print('2 : 0.125℃,')
    print('3 : 0.0625℃,')
    cmd_num = eval(input('Input number:'))
    if(cmd_num not in [0,1,2,3]):
        print('Input error!')
        sys.exit()
    print('precision selected:',precision[cmd_num])
    cmd = wr_cmd[cmd_num]
    while True:
        bus.write_byte_data(address, 0x2, cmd)
        time.sleep(1) #MIN ~ 0.061
        HighByte = bus.read_byte_data(address, 0x2)
        LowByte = bus.read_byte_data(address, 0x3)
        data = (HighByte << 8) + LowByte
        if(HighByte >= 0xF8):
            data = data - 65536 #2**16
        Temp = data * 0.0625
        print('Tempature:', Temp, '℃')
        #time.sleep(2)
except KeyboardInterrupt:
    pass
bus.close()
print('The end!')
