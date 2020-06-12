import numpy as np
import os

DIRECTORY = '/home/pi/CarData/raw'
FILE = 'home/pi/CarData/main.npz'
BACKUP = 'home/pi/CarData/main.npz.backup'


class SpdPwrConvertor:
    def __init__(self):
        """
        npz应该有101*2个元素
        """
        with open(FILE, 'rb') as f:
            temp_npz = np.load(f)
        self.l_array = temp_npz["l_array"]
        self.r_array = temp_npz["r_array"]

    @staticmethod
    def __calc_power(self, array: np.ndarray, speed):
        if int(speed) == 100:
            return array[100]
        else:
            return array[int(speed)] + (speed - int(speed))(array[int(speed) + 1] - array[int(speed)])

    def calc_l_power(self, speed):
        return self.__calc_power(self.l_array, speed)

    def calc_r_power(self, speed):
        return self.__calc_power(self.r_array, speed)

    @staticmethod
    def write_main_npz(l_array, r_array):
        if os.path.exists(FILE):
            os.popen("mv " + FILE + " " + BACKUP)
        np.savez(FILE, l_array=l_array, r_array=r_array)
