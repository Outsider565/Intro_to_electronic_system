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
    t_0=time.perf_counter()
    t_now=0
    while t_now<10:
        digitalVal=ADC0832.getResult_original()
        y.append(3.3*float(digitalVal)/255)
        t_now=time.perf_counter()-t_0
        x.append(t_now) 
        # or time.process_time()
        n=n+1
    # or time.process_time()
    print("time: ",x[-1])
    plt.plot(x,y)
    plt.show()
if __name__=='__main__':
    init()
    loop()
    ADC0832.destroy()
    print("The End")
    
    
