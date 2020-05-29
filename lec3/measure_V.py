import ADC0832
import time
def init():
	ADC0832.setup()
	#def setup(cs=11,clk=12,dio=13):
	#	global ADC_CS, ADC_CLK, ADC_DIO
	#	ADC_CS=cs
	#	ADC_CLK=clk
	#	ADC_DIO=dio
	#	GPIO.setwarnings(False)
	#	GPIO.setmode(GPIO.BOARD)			
	#	GPIO.setup(ADC_CS, GPIO.OUT)		
	#	GPIO.setup(ADC_CLK, GPIO.OUT)		
def loop():
	while True:
		digitalVal=ADC0832.getResult()
		# Get ADC result, input channal
		# getResult()函数代码实现ADC0832工作原理
		# 得到0~255之间的一个数
		# 详细参见ADC0832.py
		print(3.3*float(digitalVal)/255)
		# 转换为电压量
		time.sleep(0.2)
if __name__=='__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt:
		ADC0832.destroy()#调用GPIO.cleanup
		print("The end!")


