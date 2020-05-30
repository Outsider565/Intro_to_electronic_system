import ADC0832
import DAC_TLC5620 as DAC
import time
import numpy as np
import matplotlib.pyplot as plt

def init():
    ADC0832.setup()
    DAC.setup()
    
def loop():
    while 1:
        digitalVal=ADC0832.getResult()
        # Call some functions for signal processing
        DAC.SendOneData(digitalVal)
        
if __name__=='__main__':
    init()
    loop()
    ADC0832.destroy()
    DAC.destroy()
    print("The end!")