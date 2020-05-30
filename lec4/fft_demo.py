import numpy as np 
import matplotlib.pyplot as plt 
from scipy.signal import find_peaks
def func(x):
    w=2*np.pi
    return np.sin(2*w*x)+(-1)**np.ceil(x)#+np.sin(2*w*x)+np.sin(10*w*x)+np.sin(100*w*x)
if __name__ == "__main__":
    x=np.linspace(0,10,2560)
    w=np.pi
    y=np.abs(np.fft.fft(func(x)))
    feq=np.fft.fftfreq(2560,d=1/2560*10)
    index=find_peaks(y,threshold=0.5*y.max())[0]
    print(index)
    print(feq[index])
    np.fft.ifft(y)
    plt.plot(feq,y)

    plt.show()