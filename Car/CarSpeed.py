import threading
import time

import RPi.GPIO as GPIO

LS = 6
RS = 12


class SpeedGetter(threading.Thread):
    def __init__(self, l_timer: list, r_timer: list, t0: float):
        super().__init__()
        self._stop_event = threading.Event()
        self.t0 = t0

        self.l_timer = l_timer
        self.r_timer = r_timer

    def stop(self):
        self._stop_event.set()

    def join(self, *args, **kwargs):
        self.stop()
        super(SpeedGetter, self).join(*args, **kwargs)

    def run(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([LS, RS], GPIO.IN)
        GPIO.add_event_detect(
            LS, GPIO.RISING, callback=self.insert_timer)
        GPIO.add_event_detect(
            RS, GPIO.RISING, callback=self.insert_timer)
        while not self._stop_event.is_set():
            time.sleep(0.2)

    def insert_timer(self, channel):
        lock = threading.Lock()
        lock.acquire()
        if channel == LS:
            self.l_timer.append(time.perf_counter() - self.t0)
        elif channel == RS:
            self.r_timer.append(time.perf_counter() - self.t0)
        lock.release()


class CarSpeed:
    def __init__(self, t0=None, period=0.2):
        self.period = period
        self.l_timer = []
        self.r_timer = []
        if t0 is None:
            self.t0 = time.perf_counter()
        self.speed_getter = SpeedGetter(self.l_timer, self.r_timer, self.t0)
        self.speed_getter.start()

    @staticmethod
    def __get_time_index(time_list: list, t: float):
        start = 0
        end = len(time_list) - 1
        while True:
            mid = (start + end) // 2
            if time_list[mid] <= t <= time_list[mid + 1]:
                return mid, mid + 1
            elif t < time_list[mid]:
                end = mid
            elif time_list[mid] < t:
                start = mid

    def __get_speed(self, time_list: list, t: float, length=4):
        """
        右轮
        :param t:时间
        :return: 转速(每秒所转的次数)
        """
        if t is None:
            t = time.perf_counter() - self.t0

        if len(time_list) == 0:
            return 0
        if t > time_list[-1] + self.period:
            return 0
        elif t <= time_list[0]:
            return 0
        elif time_list[-1] + self.period > t >= time_list[-1]:
            index = (len(time_list) - 1 - length, len(time_list) - 1)
            i_range = 0
            t1 = time_list[max(index[0], 0)]
            t2 = t
        else:
            index = self.__get_time_index(time_list, t)
            assert index != -1
            i_range = min((length, len(time_list) - index[1] - 1, index[0]))
            t1 = time_list[index[0] - i_range]
            t2 = time_list[index[1] + i_range]
        try:
            return (index[1] - index[0] + 2 * i_range) / (t2 - t1) / 10
        except ZeroDivisionError:
            return 0

    def get_l_speed(self, t=None):
        return self.__get_speed(self.l_timer, t)

    def get_r_speed(self, t=None):
        return self.__get_speed(self.r_timer, t)

    def __get_times(self, time_list, t):
        if t is None:
            t = time.perf_counter() - self.t0
        if len(time_list) == 0:
            return 0
        elif t < time_list[0]:
            return 0
        elif t >= time_list[-1]:
            return len(time_list)
        else:
            return self.__get_time_index(time_list, t)[1]

    def get_l_round(self, t=None):
        return self.__get_times(self.l_timer, t) / 10

    def get_r_round(self, t=None):
        return self.__get_times(self.r_timer, t) / 10


if __name__ == '__main__':
    c = CarSpeed()
    time.sleep(5)
