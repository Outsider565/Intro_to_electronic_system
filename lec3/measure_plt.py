import ADC0832
import time
import numpy as np
import matplotlib.pyplot as plt
def init():
	ADC0832.setup()
def loop():
	n=0
	i=0
	y=[]
	x=[]
	t=time.process_time() 

	while n<10:
		digitalVal=ADC0832.getResult()
		y.append(3.3*float(digitalVal)/255)
		x.append(time.process_time()) 
		n=n+1
	#plt.axis([0.1,0.2,0.4,0.8])
	#前后两组参数分别表示x、y轴范围
	#等价于plt.xlim(0.1,0.2) plt.ylim(0.4,0.8)
	plt.plot(x,y,'-o')
	while i<10:
		x1="%.3f"%x[i]
		y1="%.2f"%y[i]
		text='{'+str(x1)+','+str(y1)+'}'
		plt.text(x[i],y[i],text)
		i=i+1
	plt.show()
if __name__=='__main__':
	init()
	loop()
	ADC0832.destroy()
	print("The End")
	
	