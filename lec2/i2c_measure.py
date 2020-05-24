import time
import smbus
import numpy as np
import matplotlib.pyplot as plt
DISTANCE = 0xb0
TIME = 0xb2
DISTANCE_WITH_TEMP = 0xb4
TEMP = 0xca
LIGHT = 0xa0


class dataGetter():
    def __init__(self, address, wr_cmd):
        self.addr = address
        self.wr_cmd = wr_cmd
        self.bus = None

    def init_SMBUS(self):
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(self.addr, 0x2, self.wr_cmd)
        time.sleep(1)

    def get(self):
        """
        返回值，两个字节的数据
        如果是距离的话，则为mm
        如果是时间，则为us
        如果是温度，则为0.0625度，其中前5位为符号位
        如果是光强，则为0-1023之间
        """
        HighByte, LowByte = self.bus.read_byte_data(
            self.addr, 0x2), self.bus.read_byte_data(self.addr, 0x3)
        return (HighByte << 8) + LowByte

    def free(self):
        self.bus.close()


def test_speed(plot=False):
    disList=[]
    vList=[]
    timeList=[]
    try:
        getter = dataGetter(0x74, DISTANCE)
        for i in range(1000):
            getter.init_SMBUS()
            time.sleep(0.05)
            t=time.perf_counter()
            x=getter.get()
            if len(disList)!=0 :
                v=(x-disList[i-1])/(t-timeList[i-1])
                print("x: {:.1f}mm, v: {:.1f}mm/s".format(x,v))
                vList.append(v)
            timeList.append(t)
            disList.append(x)
    except KeyboardInterrupt:
        getter.free()
    finally:
        vArray=np.array(vList)
        t_0=timeList[0]
        timeList=list(map(lambda x:x-t_0,timeList))
        print("v_mean = {:.2f}mm/s".format(vArray.mean()))
        print("speed_mean = {:.2f}mm/s".format(np.abs(vArray).mean()))
        if plot is True:
            plt.figure("x-t,v-t")
            plt.plot(timeList[1:],vList,label="v\\mm/s")
            plt.plot(timeList[1:],disList[1:],label="x\\mm")
            plt.legend()
            plt.show()

def test_temp():
    disList=[]
    try:
        getter = dataGetter(0x74, TEMP)
        for i in range(10):
            getter.init_SMBUS()
            time.sleep(0.05)
            a=getter.get()*0.0625
            print("{:.1f}".format(a),end=',')
            disList.append(a)

    except KeyboardInterrupt:
        getter.free()
    finally:
        array=np.array(disList)
        print("mean: {:.2f}".format(vArray.mean()))
        print("over")
if __name__ == "__main__":
    test_speed(plot=True)
