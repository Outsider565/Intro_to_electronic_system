import threading

import numpy as np
import wiringpi

import CarCtrl
import Carlog

logger = Carlog.logger
FACTOR = 7  # 排除超声意外情况的Threshold
SIDE = 1  # 超声传感器是放在左边还是右边，只能为1或-1
LIMIT = 10  # 如果测得的距离差小于该值，同意插入DiffList
SIZE = 3  # 求当前位置时，选用SIZE个最近的距离差求平均值，越大越稳定，越小越灵敏 <=5


class DiffList:
    """
    为了排除超声传感器的特殊情况和通过消防门时的特殊情况
    """

    def __init__(self):
        self.lst = []

    def append(self, val):
        """
        在距离差分列表中插入一个值，并判断该值的有效性，如果有效则插入，返回True，否则返回False，且不插入
        """
        if self.if_valid(val):
            self.lst.append(val)
            return True
        else:
            logger.info("Unusual Fluctuation: " +
                        str(self.__mean_abs_10_elem()) + "->" + str(val))
            return False

    def __mean_abs_10_elem(self):
        """
        求最近10个值的绝对值的平均
        """
        return np.abs(np.array(self.lst[-10:])).mean()

    def if_valid(self, val):
        if len(self.lst) < 5 or self.__mean_abs_10_elem() == 0 or abs(val) <= FACTOR * self.__mean_abs_10_elem() or abs(
                val) < LIMIT:
            return True
        else:
            return False

    def get_sum(self):
        """
        :return: 求I，直接把整个数列求和
        """
        return np.array(self.lst).sum()

    def get_val(self):
        """
        :return: 求P，选取最后SIZE个距离差，求平均数
        """
        if len(self.lst) == 0:
            return 0
        if len(self.lst) <= SIZE:
            return np.array(self.lst).mean()
        else:
            logger.debug(str(self.lst[-10:]))
            return np.array(self.lst[-SIZE:]).mean()

    def get_d(self):
        """
        :return: 求D，直接对最近的两个值求差分
        """
        if len(self.lst) < 5:
            return 0
        else:
            return self.lst[-1] - self.lst[-2]

    def __getitem__(self, item):
        return self.lst[item]

    def __str__(self):
        return str(self.lst)


class CarForward:
    def __init__(self, period=0.1, kp=0.020, ki=0.004, kd=0.005, speed=100, init_val=0.2):
        """
        :param period: 整个调节的更新周期
        :param init_val: PID调节的初始量，一般设为0，如果遇到电池/开始没有放正的问题再进行调整
        """
        self.car = CarCtrl.CarCtrl(speed=0, init_time=0)
        self.car.start()
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.speed = speed
        logger.info("Wait 1 second for initiation")
        # 或许可以先把马达开到0.2预热啥的...
        # self.car.set_power(10)
        self.car.stay(1)
        base_distance = np.array(self.car.basis.dist_list).mean()
        logger.info("base distance：{:.1f}".format(base_distance))
        self.diff_list = DiffList()
        self.init_val=init_val
        self.period = period
        self.__end_flag = threading.Event()  # 线程结束的标志，这是线程安全的
        self.__init_record_diff_list()
        self.__init_run()

    def update_diff_list(self):
        while not self.__end_flag.isSet():
            self.diff_list.append(
                self.car.get_distance() - self.car.get_distance(1))
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
                        self.kd * self.diff_list.get_d()) * SIDE + self.init_val
                pid_info = "p: {:.3f}".format(self.kp * self.diff_list.get_val()) + '\t' + "i: {:.3f}".format(
                    self.ki * self.diff_list.get_sum()) + '\t' + "d: {:.3f}".format(self.kd * self.diff_list.get_d())
                logger.info("distance change: {:.1f}".format(self.diff_list.get_val()))
                logger.debug(pid_info)
                logger.info("set bias as: {:.3f}".format(bias))

                self.car.set_expected_diff(bias)
                self.car.stay(0.1)
        except Exception as e:
            logger.error(str(e))
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
        f.stay(16)
        f.stop()
    except Exception as e:
        logger.error(str(e))
        f.stop()
