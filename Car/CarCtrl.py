import CarInfo
import threading
import numpy as np


class CarCtrl:
    def __init__(self, speed=100, diff=0, period=0.05, kp=66, ki=15, kd=2):
        self.period = period
        self.basis = CarInfo.CarInfo(period)
        self.expected_diff = diff
        self.power = speed
        self.bias = 0
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.__end_flag = threading.Event()

    def set_expected_diff(self, val):
        self.expected_diff = val

    def set_power(self, val):
        self.power = val

    def get_p_diff(self, t=None):
        return (self.basis.get_r_round(t) - self.basis.get_l_round(t) - self.expected_diff) * self.kp

    def get_i_diff(self):
        self.basis.update_speed_and_round()
        if len(self.basis.r_round) == 0:
            return - self.expected_diff
        else:
            return ((np.array(self.basis.r_round).sum() - np.array(
                self.basis.l_round).sum()) / (len(self.basis.r_round)) - self.expected_diff) * self.ki

    def get_d_diff(self):
        return (self.get_p_diff(self.basis.get_time()) - self.get_p_diff(
            self.basis.get_time() - 1.5 * self.period)) * self.kd

    def get_diff(self):
        return self.get_p_diff() + self.get_d_diff() + self.get_i_diff()

    def get_time(self):
        return self.basis.get_time()

    def get_round(self):
        return min(self.basis.get_l_round(), self.basis.get_r_round())

    def __run(self):
        while not self.__end_flag.isSet():
            self.basis.set_left_power(max(self.power + min(self.get_diff(), 0), 0))
            self.basis.set_right_power(max(self.power - max(self.get_diff(), 0), 0))
            self.print_info()
            self.basis.stay(self.period)

    def start(self):
        run_thread = threading.Thread(target=self.__run)
        run_thread.start()

    def stop(self):
        self.__end_flag.set()
        self.basis.free()

    def print_info(self):
        print("l_round:" + '{:.1f}'.format(self.basis.get_l_round()) + "\tr_round: " + '{:.1f}'.format(
            self.basis.get_r_round()))
        print("l_power:" + '{:.1f}'.format(self.basis.get_l_power()) + "\tr_power: " + '{:.1f}'.format(
            self.basis.get_r_power()))
        print("p: " + "{:.2f}".format(self.get_p_diff()) + "\ti: " + "{:.2f}".format(
            self.get_i_diff()) + "\td: " + "{:.2f}".format(self.get_d_diff()))
        print("dist: ", self.basis.get_distance())

    def get_distance(self, index=0):
        return self.basis.get_distance(index)

    @staticmethod
    def stay(t):
        CarInfo.CarInfo.stay(t)

    def set_r_mode(self):
        self.basis.set_r_mode()


if __name__ == '__main__':
    try:
        c = CarCtrl()
        c.start()
        c.set_power(70)
        c.stay(1)
        c.set_power(100)
        c.set_expected_diff(0)
        c.stay(3)
        # c.set_r_mode()
        # c.stay(3)
        # c.set_expected_diff()
        c.stop()
    except:
        c.stop()
