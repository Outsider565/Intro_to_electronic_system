import CarCtrl
import numpy as np
import threading
import wiringpi

FACTOR = 7  # 排除超声意外情况的Threshold
SIDE = 0.3  # 超声传感器是放在左边还是右边


class DiffList:
    """
    为了排除超声传感器的特殊情况和通过消防门时的特殊情况
    """

    def __init__(self):
        self.lst = []

    def append(self, val):
        if self.if_valid(val):
            if len(self.lst) < 10:
                self.lst.append(val)
            elif len(self.lst) == 10:
                self.lst.pop(0)
                self.lst.append(val)
            else:
                raise IndexError
        else:
            print("Unusual Fluctuation: " +
                  str(self.lst[-1]) + "->" + str(val))

    def __mean_abs(self):
        return np.abs(np.array(self.lst)).mean()

    def if_valid(self, val):
        if len(self.lst) < 5 or self.__mean_abs() == 0 or abs(val) <= FACTOR * self.__mean_abs():
            return True
        else:
            return False

    def get_val(self):
        if len(self.lst) == 0:
            return 0
        if len(self.lst) <= 5:
            return np.array(self.lst).mean()
        else:
            return np.array(self.lst[:-5]).mean()

    def __getitem__(self, item):
        return self.lst[item]

    def __str__(self):
        return str(self.lst)


class CarForward:
    def __init__(self, period=0.1, kp=0.01, ki=0.008, speed=100):
        self.car = CarCtrl.CarCtrl(speed=0)
        self.car.start()
        self.kp = kp
        self.ki = ki
        self.speed = speed
        print("Wait 1 second for initiation")
        # TODO:或许可以先把马达开到0.2预热啥的...
        # self.car.set_power(10)
        self.car.stay(1)
        self.base_distance = np.array(self.car.basis.dist_list).mean()
        print(self.car.basis.dist_list)
        print("wait xxx")
        self.diff_list = DiffList()
        self.dist_list=DiffList()
        self.period = period
        self.__end_flag = threading.Event()
        self.__init_record_diff_list()
        self.__init_run()

    def update_diff_list(self):
        while not self.__end_flag.isSet():
            self.diff_list.append(
                self.car.get_distance() - self.car.get_distance(1))
            self.dist_list.append(self.car.get_distance())
            wiringpi.delay(int(1000 * self.period))

    def __init_record_diff_list(self):
        diff_list_thread = threading.Thread(target=self.update_diff_list)
        diff_list_thread.start()

    def __init_run(self):
        run_thread = threading.Thread(target=self.run)
        run_thread.start()

    def run(self):
        try:
            self.car.set_power(self.speed)
            while not self.__end_flag.isSet():
                bias = (self.kp * self.diff_list.get_val() + self.ki *
                        (self.base_distance - self.dist_list.get_val()))*SIDE
                print("{:.3f}".format(self.kp * self.diff_list.get_val()),"{:.3f}".format(self.ki *
                        (self.base_distance - self.dist_list.get_val())))
                print("set bias as: {:.3f}".format(bias))
                self.car.set_expected_diff(bias)
                self.car.stay(0.1)
        except:
            self.stop()

    def stay(self, t):
        self.car.stay(t)

    def stop(self):
        self.__end_flag.set()
        self.car.stop()


if __name__ == '__main__':
    f = CarForward(speed=100)
    f.stay(7)
    f.stop()
