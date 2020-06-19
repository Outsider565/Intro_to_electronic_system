import threading

import numpy as np

import CarBasis
import Carlog

logger = Carlog.logger


class CarCtrl:
    """
    该类承担了整个小车最重的责任，进行PID调节小车的方向
    """
    def __init__(self, speed=100, expected_diff=0, period=0.05, kp=80, ki=0.95, kd=1.2, init_l_speed=100,
                 init_r_speed=78, init_time=0.1, i_init_value=60):
        """
        :param speed: 希望小车以多少PWM功率运行
        :param expected_diff: 希望小车左轮和右轮转圈数的差值
        :param period: 系统更新的周期
        :param init_l_speed: 初始左轮速度
        :param init_r_speed: 初始右轮速度
        :param init_time: 初始时间
        :param i_init_value: 最开始给i的初值（因为左轮和右轮的转速差异，需要给一个初始值来利用PID迭代
        """
        self.period = period
        self.basis = CarBasis.CarBasis(period)
        self.expected_diff = expected_diff
        self.power = speed
        self.bias = 0
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.p_diff = 0
        self.i_diff = 0
        self.d_diff = 0
        self.init_l_speed = init_l_speed
        self.init_r_speed = init_r_speed
        self.init_time = init_time
        self.i_init_value = i_init_value
        self.raw_diff_list = []
        self.__end_flag = threading.Event()

    def set_expected_diff(self, val):
        self.expected_diff = val

    def set_power(self, val):
        self.power = val

    def get_p_diff(self, t=None):
        ans = (self.basis.get_r_round(t) - self.basis.get_l_round(t) - self.expected_diff)
        if t is None:
            self.raw_diff_list.append(ans)
        self.p_diff = ans * self.kp
        return ans * self.kp

    def get_i_diff(self):
        self.basis.update_speed_and_round()
        if len(self.raw_diff_list) == 0:
            return 0  # 此时默认小车按正常方向行走
        else:
            self.i_diff = np.array(self.raw_diff_list).sum() * self.ki
            return np.array(self.raw_diff_list).sum() * self.ki

    def get_d_diff(self):
        self.d_diff = (self.get_p_diff(self.basis.get_time()) - self.get_p_diff(
            self.basis.get_time() - 1.5 * self.period)) * self.kd
        return (self.get_p_diff(self.basis.get_time()) - self.get_p_diff(
            self.basis.get_time() - 1.5 * self.period)) * self.kd

    def get_diff(self):
        return self.get_p_diff() + self.get_d_diff() + self.get_i_diff()

    def get_time(self):
        return self.basis.get_time()

    def get_round(self):
        return min(self.basis.get_l_round(), self.basis.get_r_round())

    def __run(self):
        """
        会先在无指引的情况下运行self.period s，并且给raw然后再进入PID调控
        :return:
        """
        self.raw_diff_list.append(self.i_init_value)
        while not self.__end_flag.isSet():
            try:
                if self.get_time() <= self.init_time:  # 在真正启动前不print相关信息
                    self.basis.set_left_power(self.init_l_speed)  # 最开始的小车运作不依靠PID，而依靠手动调节
                    self.basis.set_right_power(self.init_r_speed)
                    self.basis.stay(self.period)
                else:
                    self.basis.set_left_power(max(self.power + min(self.get_diff(), 0), 0))
                    self.basis.set_right_power(max(self.power - max(self.get_diff(), 0), 0))
                    self.print_info()
                    self.basis.stay(self.period)
            except Exception as e:
                self.basis.set_left_power(100)
                self.basis.set_right_power(60)
                logger.error("Run into exception: " + str(e))
                self.print_info()
                self.basis.stay(self.period)

    def start(self):
        run_thread = threading.Thread(target=self.__run)
        run_thread.start()

    def stop(self):
        self.__end_flag.set()
        self.basis.free()

    def print_info(self):
        if self.basis.get_l_round() != 0 or self.basis.get_r_round() != 0:
            logger.info("l_round:" + '{:.1f}'.format(self.basis.get_l_round()) + "\tr_round: " + '{:.1f}'.format(
                self.basis.get_r_round()))
            logger.debug("l_power:" + '{:.1f}'.format(self.basis.get_l_power()) + "\tr_power: " + '{:.1f}'.format(
                self.basis.get_r_power()))
            logger.debug("p_power: " + "{:.2f}".format(self.p_diff) + "\ti_power: " + "{:.2f}".format(
                self.i_diff) + "\td_power: " + "{:.2f}".format(self.d_diff))
            logger.debug("raw_distance: " + str(self.get_distance()))

    def get_distance(self, index=0):
        return self.basis.get_distance(index)

    @staticmethod
    def stay(t):
        CarBasis.CarBasis.stay(t)

    def set_r_mode(self):
        self.basis.set_r_mode()


if __name__ == '__main__':
    try:
        c = CarCtrl()
        c.start()
        c.set_power(100)
        c.stay(4)
        # c.set_expected_diff(0.1)
        # c.stay(3)
        # c.set_r_mode()
        # c.stay(3)
        # c.set_expected_diff()
        c.stop()
    except:
        c.stop()
