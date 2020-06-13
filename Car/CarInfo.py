import CarPower as power
import CarSpeed as speed
import CarUltra as ultra
import time
import numpy as np
import threading
import wiringpi

DIRECTORY = '/home/pi/CarData/raw'


class CarInfo(power.CarPower, speed.CarSpeed, ultra.CarUltra):
    def __init__(self, period=0.05):
        """
        这是用于获取和记录小车信息的类
        :param period: 每隔多久测一次
        """
        self.t0 = time.perf_counter()
        power.CarPower.__init__(self)
        speed.CarSpeed.__init__(self, t0=self.t0)
        ultra.CarUltra.__init__(self, period=period)
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
            self.dist_list.append(self.get_raw_distance())

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
        print("data write into " + DIRECTORY + "/" + t_name + ".npz")
        try:
            with open(DIRECTORY + "/" + t_name + ".npz", "wb") as f:
                np.savez(f, time_list=time_list, l_speed=l_speed_n, r_speed=r_speed_n, l_power=l_power_n,
                         r_power=r_power_n,
                         l_round=l_round_n, r_round=r_round_n, dist_list=dist_n)
        except:
            print("Write Failed")
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
        return time.perf_counter() - self.t0

    def get_distance(self, index=0):
        if len(self.dist_list) <= index:
            return 0
        else:
            return self.dist_list[-1*index]


def gen_raw_data():
    c = CarInfo(0.1)
    c.free()
    try:
        for i in range(0, 101, 2):
            c.set_left_power(i)
            c.set_right_power(i)
            c.stay(3)
            print(i, c.get_l_speed(), c.get_r_speed())
            c.set_left_power(0)
            c.set_right_power(0)
            c.stay(1)
        for i in range(-100, 101):
           c.set_right_power(i)
           c.stay(3)
           print(i, c.get_l_speed(), c.get_r_speed())
           c.set_right_power(0)
           c.stay(1)
           c.free()
    except:
        print("Failed")
        c.save_data()
        c.free()


if __name__ == '__main__':
    c = CarInfo(0.1)
    spd = 100
    c.set_both_power(spd)
    c.set_r_mode()
    while c.get_time() < 19:
        c.set_left_power(spd * (1 - min(max(c.get_l_round() - c.get_r_round(), 0), 1)))
        c.set_right_power(spd * (1 - min(max(c.get_r_round() - c.get_l_round(), 0), 1)))
        c.stay(0.1)
        print("Round:", c.get_l_round(), c.get_r_round())
        print("Power:", c.get_l_power(), c.get_r_power())
    # while c.get_l_round()<13.3:
    #    c.set_left_power(-1*spd)
    #    c.set_right_power(spd)
    #    c.stay(0.05)
    #    print(c.get_l_round(),c.get_r_round())
    c.save_data()
    c.free()
