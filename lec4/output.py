import ADC0832
import DAC_TLC5620 as DAC
import time
import numpy as np
import matplotlib.pyplot as plt
import wiringpi
MAX=220
MIN=10

def init():
    ADC0832.setup()
    DAC.setup()


def getGraph(upperFunc, lowerFunc, size):
    """
    upperFunc/lowerFunc: accept para in [0,1], return in (0,255)
    """
    res = np.ones(shape=size,dtype=np.uint8)
    for i in range(size):
        if i & 1 == 1:
            res[i] = upperFunc(i/size)
        else:
            res[i] = lowerFunc(i/size)
    return res

def heart_upFunc(x):
    x=x*4-2
    return np.sqrt(1-(np.abs(x)-1)**2)*50+170

def heart_lwFunc(x):
    x=x*4-2
    return (np.arccos(1-np.abs(x))-np.pi)*50+170

def I_upFunc(x):
    x=x*2-1
    if x<-0.1 or x>0.1:
        return MIN
    else:
        return MAX

def I_lwFunc(x):
    return MIN

def blank(x):
    return MIN

def U_upFunc(x):
    x=x*2-1
    if x<-0.7 or x>0.7:
        return MIN
    elif x<-0.5 or x>0.5:
        return MAX
    else:
        return x**2*MAX*0.3+MIN+10
    
def U_lwFunc(x):
    x=x*2-1
    if x<-0.7 or x>0.7:
        return MIN
    else:
        return x**2*MAX*0.3

def ILOVEU_upFunc(x):
    if x<1/5:
        return blank(x)
    elif x<2/5:
        return I_upFunc(5*x-1)
    elif x<3/5:
        return heart_upFunc(x*5-2)
    elif x<4/5:
        return U_upFunc(x*5-3)
    else:
        return blank(x)

def ILOVEU_lwFunc(x):
    if x<1/5:
        return blank(x)
    elif x<2/5:
        return I_lwFunc(5*x-1)
    elif x<3/5:
        return heart_lwFunc(x*5-2)
    elif x<4/5:
        return U_lwFunc(x*5-3)
    else:
        return blank(x)


def outputGraph(graph,time):
    while 1:
        for i in graph:
            DAC.SendOneData(i)
            wiringpi.delayMicroseconds(time)

if __name__ == "__main__":
    DAC.setup()
    res=getGraph(ILOVEU_upFunc,ILOVEU_lwFunc,1000)
    outputGraph(res,2)
    #plt.plot(np.linspace(0,1,1000),res)
   # plt.show()