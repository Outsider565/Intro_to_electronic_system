import time
import smbus
import wiringpi
DISTANCE = 0xb0
TIME = 0xb2
DISTANCE_WITH_TEMP = 0xb4
TEMP = 0xca
LIGHT = 0xa0


class CarUltra:
    def __init__(self, address=0x74, wr_cmd=DISTANCE_WITH_TEMP,period=0.1):
        self.addr = address
        self.wr_cmd = wr_cmd
        self.bus = smbus.SMBus(1)
        self.period=period

    def get_distance(self):
        self.bus.write_byte_data(self.addr, 0x2, self.wr_cmd)
        wiringpi.delay(100)
        high_byte, LowByte = self.bus.read_byte_data(
            self.addr, 0x2), self.bus.read_byte_data(self.addr, 0x3)
        return (high_byte << 8) + LowByte

    def free(self):
        self.bus.close()


if __name__ == '__main__':
    addr=0x74
    c=CarUltra(period=0.05)
    for i in range(10):
        print(c.get_distance())
