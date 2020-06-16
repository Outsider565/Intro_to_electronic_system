import logging
import time

# 创建对象
DIRECTORY = '/home/pi/CarData/log'
t_name = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
logger = logging.getLogger()  # 创建一个logging对象
file_handler = logging.FileHandler(DIRECTORY + "/" + t_name + '.log', encoding="utf-8")  # 创建一个文件对象
shell_handler = logging.StreamHandler()  # 创建一个屏幕对象

# 创建配置显示格式同时导入文件对象和屏幕对象中
formatter1 = logging.Formatter('%(asctime)s: %(message)s', '%I:%M:%S')
formatter2 = logging.Formatter("%(asctime)s %(message)s", '%I:%M:%S')
file_handler.setFormatter(formatter1)
shell_handler.setFormatter(formatter2)

# 将配置好的文件格式和屏幕格式导入logging对象中
logger.addHandler(file_handler)
logger.addHandler(shell_handler)

# 总开关
logger.setLevel(logging.NOTSET)  # 设置基础显示等级
file_handler.setLevel(logging.DEBUG)  # 设置文件显示等级
shell_handler.setLevel(logging.INFO)  # 设置屏幕显示等级

if __name__ == '__main__':
    logger.debug("x")
