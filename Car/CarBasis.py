import threading
import time

import numpy as np
import wiringpi

import CarPower as power
import CarSpeed as speed
import CarUltra as ultra
import Carlog

DIRECTORY = '/home/pi/CarData/raw'
logger = Carlog.logger


class CarBasis(power.CarPower, speed.CarSpeed):
    def __init__(self, period=0.05):
        """
        这是封装小车底层和记录相关信息的类，继承了CarPower和CarSpeed中的全部接口
        :param period: 每隔多久测一次
        """
        self.t0 = time.perf_counter()
        power.CarPower.__init__(self)
        speed.CarSpeed.__init__(self, t0=self.t0)
        self.ultra_getter = ultra.CarUltra(period=0.1)
        self.period = period
        self.l_speed = []
        self.r_speed = []
        self.l_power = []
        self.r_power = []
        self.l_round = []
        self.r_round = []
        self.dist_list = []
        self.time_list = []
        self.__end_flag = threading.Event()
        self.__init_record_power()
        self.__init_record_dist()

    def __record_power(self):
        wiringpi.delay(int(1000 * self.period))
        while not self.__end_flag.is_set():
            self.l_power.append(self.get_l_power())
            self.r_power.append(self.get_r_power())
            wiringpi.delay(int(1000 * self.period))

    def __record_distance(self):
        while not self.__end_flag.is_set():
            self.dist_list.append(self.ultra_getter.get_raw_distance())

    def __init_record_power(self):
        record_thread = threading.Thread(target=self.__record_power)
        record_thread.start()

    def __init_record_dist(self):
        record_thread = threading.Thread(target=self.__record_distance)
        record_thread.start()

    def save_data(self):
        self.update_speed_and_round()
        time_list = np.array(self.time_list)
        l_speed_n = np.array(self.l_speed)
        r_speed_n = np.array(self.r_speed)
        dif = len(r_speed_n) - len(self.l_power)
        l_power_n = np.array(self.l_power[:-1 * dif])
        r_power_n = np.array(self.r_power[:-1 * dif])
        l_round_n = np.array(self.l_round)
        r_round_n = np.array(self.r_round)
        dist_n = np.array(self.dist_list)
        t_name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
        logger.info("l_power: {:.3f}\tr_power: {:.3f}".format(np.delete(l_power_n, np.where(l_power_n == 0)).mean(),
                                                              np.delete(r_power_n, np.where(r_power_n == 0)).mean()))
        logger.info("l_speed: {:.3f}\tr_speed: {:.3f}".format(np.delete(l_speed_n, np.where(l_speed_n == 0)).mean(),
                                                              np.delete(r_speed_n, np.where(r_speed_n == 0)).mean()))
        logger.info("data write into " + DIRECTORY + "/" + t_name + ".npz")
        try:
            with open(DIRECTORY + "/" + t_name + ".npz", "wb") as f:
                np.savez(f, time_list=time_list, l_speed=l_speed_n, r_speed=r_speed_n, l_power=l_power_n,
                         r_power=r_power_n,
                         l_round=l_round_n, r_round=r_round_n, dist_list=dist_n)
        except Exception as e:
            logger.error("Write Failed: ", e)
            self.free()

    def update_speed_and_round(self):
        t_now = time.perf_counter() - self.t0
        t_c = (len(self.l_speed) + 1) * self.period
        while t_c < t_now:
            self.time_list.append(t_c)
            self.l_speed.append(self.get_l_speed(t_c))
            self.r_speed.append(self.get_r_speed(t_c))
            self.l_round.append(self.get_l_round(t_c))
            self.r_round.append(self.get_r_round(t_c))
            t_c += self.period

    def free(self):
        self.__end_flag.set()
        self.save_data()
        power.CarPower.free(self)

    def get_time(self):
        """
        :return: 从计时开始到现在的时间
        """
        return time.perf_counter() - self.t0

    def get_distance(self, index=0):
        if len(self.dist_list) <= index:
            return 0
        else:
            return self.dist_list[len(self.dist_list) - 1 - index]


def gen_raw_data():
    # 这是测试时用来生成两马达性能的函数，可以忽略
    car = CarBasis(0.1)
    try:
        for i in range(0, 101, 5):
            car.set_left_power(i)
            car.set_right_power(i)
            car.stay(3)
            print(i, car.get_l_speed(), car.get_r_speed())
            car.set_left_power(0)
            car.set_right_power(0)
            car.stay(1)
#        for i in range(-100, 101):
#           car.set_right_power(i)
#           car.stay(3)
#           print(i, car.get_l_speed(), car.get_r_speed())
#           car.set_right_power(0)
#           car.stay(1)
        car.free()
    except Exception as e:
        print(e)
        car.free()


if __name__ == '__main__':
#c = CarBasis(0.1)
# spd = 100
#   c.set_both_power(spd)
#   c.set_r_mode()
#   while c.get_time() < 19:
#       c.set_left_power(spd * (1 - min(max(c.get_l_round() - c.get_r_round(), 0), 1)))
#       c.set_right_power(spd * (1 - min(max(c.get_r_round() - c.get_l_round(), 0), 1)))
#       c.stay(0.1)
#       print("Round:", c.get_l_round(), c.get_r_round())
#       print("Power:", c.get_l_power(), c.get_r_power())
    # while c.get_l_round()<13.3:
    #    c.set_left_power(-1*spd)
    #    c.set_right_power(spd)
    #    c.stay(0.05)
    #    print(c.get_l_round(),c.get_r_round())
#   c.save_data()
#   c.free()
	gen_raw_data()
	
