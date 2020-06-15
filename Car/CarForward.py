import CarCtrl
import numpy as np
import threading
import wiringpi

FACTOR = 7  # 排除超声意外情况的Threshold
SIDE = 1  # 超声传感器是放在左边还是右边，只能为1或-1

# TODO:增加log功能
class DiffList:
    """
    为了排除超声传感器的特殊情况和通过消防门时的特殊情况
    """

    def __init__(self):
        self.lst = []

    def append(self, val):
        """
        在距离差分列表中插入一个值，并判断该值的有效性，如果有效则插入，返回True，否则返回False，且不插入
        :param val:
        :return:
        """
        if self.if_valid(val):
            self.lst.append(val)
            return True
        else:
            print("Unusual Fluctuation: " +
                  str(self.__mean_abs()) + "->" + str(val))
            return False

    def __mean_abs(self):
        return np.abs(np.array(self.lst[-10:])).mean()

    def if_valid(self, val):
        if len(self.lst) < 5 or self.__mean_abs() == 0 or abs(val) <= FACTOR * self.__mean_abs():
            return True
        else:
            return False

    def get_sum(self):
        return np.array(self.lst).sum()

    def get_val(self):
        if len(self.lst) == 0:
            return 0
        if len(self.lst) <= 5:
            return np.array(self.lst).mean()
        else:
            return np.array(self.lst[:-5]).mean()

    def get_d(self):
        if len(self.lst) < 5:
            return 0
        else:
            return self.lst[-1] - self.lst[-2]

    def __getitem__(self, item):
        return self.lst[item]

    def __str__(self):
        return str(self.lst)


class CarForward:
    def __init__(self, period=0.1, kp=0.1, ki=0.005, kd=0.01, speed=100):
        self.car = CarCtrl.CarCtrl(speed=0, init_time=0, if_print=False)
        self.car.start()
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.speed = speed
        print("Wait 1 second for initiation")
        # TODO:或许可以先把马达开到0.2预热啥的...
        # self.car.set_power(10)
        self.car.stay(1)
        base_distance = np.array(self.car.basis.dist_list).mean()
        print("base distance：{:.1f}".format(base_distance))
        self.diff_list = DiffList()
        self.dist_list = DiffList()
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
                bias = (self.kp * self.diff_list.get_val() + self.ki * self.diff_list.get_sum() +
                        self.kd * self.diff_list.get_d()) * SIDE
                print("p: {:.3f}".format(self.kp * self.diff_list.get_val()) + '\t' +
                      "i: {:.3f}".format(self.ki * self.diff_list.get_sum()) + 't' +
                      "d: {:.3f}".format(self.kd * self.diff_list.get_d()))
                print("set bias as: {:.3f}".format(bias))
                self.car.set_expected_diff(bias)
                self.car.stay(0.1)
        except Exception as e:
            print(e)
            self.stop()

    def stay(self, t):
        self.car.stay(t)

    def stop(self):
        self.__end_flag.set()
        self.car.stop()

    def get_distance(self):
        return self.car.get_distance()

if __name__ == '__main__':
    try:
        f = CarForward(speed=100)
        f.stay(0.3)
        f.stop()
    except Exception as e:
        print(e)
        f.stop()
