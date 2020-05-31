import numpy as np 
import matplotlib as plt
from phyUtil import *
ADC=np.array((0.647,0.712,0.776,0.837,0.893,0.971,1.028,1.100,1.152,1.228,1.294))
SBQ=np.array((0.646,0.706,0.771,0.829,0.890,0.969,1.03,1.10,1.15,1.23,1.29))
res=ph(ADC,SBQ)
res.calc()
res.plot()
error=ADC.mean()-SBQ.mean()
print("err:",error)