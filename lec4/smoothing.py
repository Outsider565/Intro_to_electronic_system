import ADC0832
import DAC_TLC5620 as DAC
import wiringpi
import time
import numpy as np
import matplotlib.pyplot as plt

def init():
    ADC0832.setup()
    DAC.setup()
    
def loop():
    fft_size=256       # 256-point FFT
    sampl_freq=4500    # Sampling frequency is 4500Hz
    freq_low=0         # Lower cut-off frequency
    freq_high=500      # Upper cut-off frequency
    n=0
    y=[]
    t_sample=1/sampl_freq
    t=time.time()
    t0_start=t
    while n<fft_size:
        if n>0:
            dt=time.time()-t0_start
            tmp=int(1000000*(t_sample*(n+1) - dt))
            if tmp>0:
                wiringpi.delayMicroseconds(int(1000000*(t_sample*(n+1) - dt)))
        digitalVal=ADC0832.getResult()
        n=n+1
        y.append(3.3*float(digitalVal)/255)
    t=time.time()-t    # 256_point sampling    
    
    sampl_freq2= fft_size/t # Calculate the actual sampling freq.
    print("real sample_freq: %d" % sampl_freq2)
    
    y_fft=np.fft.fft(y)    # FFT
    y_fft_ampl=np.abs(y_fft)    # Amplitude spectrum
    x=np.linspace(0,t,fft_size)
    freq=np.linspace(-sampl_freq/2,sampl_freq/2,fft_size)

    low_pos=freq_low*fft_size/sampl_freq  # Normalization treatment
    high_pos=freq_high*fft_size/sampl_freq
    high_neg=fft_size-high_pos
    low_neg=fft_size-low_pos
    i=1
    smooth_fft=[y_fft[0]]  # Keep DC offset
    while i<fft_size:  # Frequency domain filtering
        if i<low_pos:  # Below the lower cut-off frequency
            smooth_fft.append(0)
            i=i+1
            continue
        if i>high_pos and i<high_neg:  # Higher than Upper cut-off frequency
            smooth_fft.append(0)
            i=i+1
            continue
        if i>low_neg:  # Below the lower cut-off frequency
            smooth_fft.append(0)
            i=i+1
            continue
        smooth_fft.append(y_fft[i])
        i=i+1
    smooth_org=np.fft.ifft(smooth_fft)   # Fourier inversion
    smooth_fft_ampl=np.abs(smooth_fft)   # Amplitude spectrum
    smooth=np.abs(smooth_org)

    plt.figure(figsize=(8,4))
    plt.subplot(221)
    plt.plot(x,y)
    plt.title(u"Time Domain (Original)")
    plt.subplot(222)
    plt.plot(freq,np.fft.fftshift(y_fft_ampl))
    plt.title(u"Frequency Domain (Original)")
    plt.subplot(223)
    plt.plot(x,smooth)
    plt.xlabel(u"t(s)")
    plt.title(u"Time Domain(smoothing)")
    plt.subplot(224)
    plt.plot(freq,np.fft.fftshift(smooth_fft_ampl))
    plt.xlabel(u"freq(Hz)")
    plt.title(u"Frequency Domain(smoothing)")
    plt.subplots_adjust(hspace=0.4)
    plt.show()

    
    
    output_count=0
    while 1:    # Output signal
        output_count+=1
        i=0
        t=time.time()
        t2_start = time.time()
        while i<fft_size:
            if i>0:
                dt=time.time()-t2_start
                #print(int(1000000*(t_sample*(n+1) - dt)))
                tmp=int(1000000*(t_sample*(i+1) - dt))
                if tmp>0:
                    wiringpi.delayMicroseconds(tmp)
                
            DAC.SendOneData(int(smooth[i]*255/3.3))
            i=i+1
        if output_count==1:
            t=time.time()-t    # 256_point sampling    
            dac_freq= fft_size/t # Calculate the actual sampling freq.
            print("real dac_freq: %d" % dac_freq)
            

if __name__=='__main__':
    init()
    loop()
    ADC0832.destroy()
    DAC.destroy()
    print("The end!")