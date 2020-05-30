import ADC0832
import time
import numpy as np
import matplotlib.pyplot as plt

def init():
    ADC0832.setup()
    
def loop():
    fft_size=256       # 256-point FFT
#    sampl_freq=5350  # Sampling frequency
    n=0
    y=[]
    t=time.time()
    while n<fft_size:
        digitalVal=ADC0832.getResult()
        n=n+1
        y.append(3.3*float(digitalVal)/255)
    t=time.time()-t
    sampl_freq = fft_size/t # Calculate the actual sampling freq.
    y_fft=np.fft.rfft(y)/fft_size    # Real signal, FFT
    y_fft_ampl=np.abs(y_fft)    # Amplitude spectrum
    x=np.linspace(0,t,fft_size)
    freq=np.linspace(0,sampl_freq/2,int(fft_size/2+1))

    plt.figure(figsize=(8,4))
    plt.subplot(211)
    plt.plot(x,y)
    plt.xlabel(u"t(s)")
    plt.title(u"Time domain")
    plt.subplot(212)
    plt.plot(freq,y_fft_ampl)
    plt.xlabel(u"freq(Hz)")
    plt.title(u"Frequency domain")
    plt.subplots_adjust(hspace=0.4)
    plt.show()

if __name__=='__main__':
    init()
    loop()
    ADC0832.destroy()
    print("The end!")