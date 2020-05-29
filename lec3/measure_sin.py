import ADC0832
import time
import numpy as np
import matplotlib.pyplot as plt
def init():
	ADC0832.setup()
def loop():
	n=0
	t=0
	y=[]
	x=[]
	while n<1000:
		digitalVal=ADC0832.getResult()
		y.append(3.3*float(digitalVal)/255)
		x.append(time.perf_counter()) 
        # or time.process_time()
		n=n+1
	t=time.perf_counter()-t 
    # or time.process_time()
	plt.plot(x,y)
	plt.show()
if __name__=='__main__':
	init()
	loop()
	ADC0832.destroy()
	print("The End")
	
	