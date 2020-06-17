import smbus
import wiringpi

import Carlog

logger = Carlog.logger

DISTANCE = 0xb0
TIME = 0x0a  # 最大探测距离为1m，返回值为微秒
DISTANCE_WITH_TEMP = 0xb4  # 虽然测量距离更准，但查询资料可知，测量温度大约会花83ms，可能会使第一个周期接不到数据
TEMP = 0xca
LIGHT = 0xa0


class CarUltra:
    def __init__(self, address=0x74, wr_cmd=DISTANCE, period=0.1):
        self.addr = address
        self.wr_cmd = wr_cmd
        self.bus = smbus.SMBus(1)
        self.period = period

    def get_raw_distance(self):
        """
        注意：该函数不能在一个周期内多次调用，否则会引起I2C的IOERROR，因此必须通过CarBasis中的接口get_distance()来获取距离
        :return: 返回距离，单位为mm
        """
        self.bus.write_byte_data(self.addr, 0x2, self.wr_cmd)
        wiringpi.delay(int(1000 * self.period))
        while True:
            try:
                high_byte, LowByte = self.bus.read_byte_data(
                    self.addr, 0x2), self.bus.read_byte_data(self.addr, 0x3)
                break
            except IOError as e:
                logger.error("First time get failed, try again: " + str(e))
                wiringpi.delay(int(1000 * self.period))
        return (high_byte << 8) + LowByte

    def free(self):
        self.bus.close()


if __name__ == '__main__':
    addr = 0x74
    c = CarUltra(period=0.1, wr_cmd=DISTANCE)
    for i in range(100):
        print(c.get_raw_distance())
    c.free()
