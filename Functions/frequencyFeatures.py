import numpy as np
from Functions.visualise import Visualisation

class fastfourierTransform:
    def __init__(self, signal, sampleFreq, lineartaper = None, 
                 plotje = None, window = None):

        signal = (signal - signal.mean()) / signal.std()
        signalLength = len(signal)                

        # Apply linear taper of %5 at each end
        if lineartaper :
            int(signalLength * 0.05 )
            signal[0:int(signalLength * 0.05 )] = (signal[0:int(signalLength * 0.05 )] / 20)
            signal[signalLength - int(signalLength * 0.05): signalLength ] = signal[signalLength - int(signalLength * 0.05): signalLength ] / 20
            
        # add x amount of zeros so that the signal is 2^x
        check = True
        zeroscounter = 512
        while (check == True):
            if (signalLength > zeroscounter):
                 zeroscounter = 2 * zeroscounter
            else:
                tot = zeroscounter - signalLength
                check = False
        signal = np.concatenate([signal, np.zeros(tot)]) 
        ncor = len(signal)
        
        # Hamming/hanning window
        if window == 'Hanning':
            w = np.hanning(len(signal)) 
        elif window == 'Hamming':
            w = np.hamming(len(signal))  
        else:
            w = 1
        
        # Creates the necessairy frequenciees
        fftsignal           = np.fft.fft(signal * w)
        freqenties          = np.fft.fftfreq(ncor, sampleFreq)
        power               = (abs(fftsignal) / ncor)
        mask                = freqenties > 0
        
        
        # Mask array to be used for power spectra
        # ignoring half the values, as they are complex conjucates of the other
        self.freqs      = freqenties
        self.power      = power
        self.fftTime   = freqenties[mask]
        self.fftValues = power[mask]
        
        if plotje:
            Visualisation.plot6(freqenties[mask], 
                                  power[mask], 
                                  title = 'Spectral Density plot ML',
                                  xlabel = 'Frequency [Hz]',
                                  ylabel = 'Power',
                                  ylim = True
                                  )

    def F50(fftValues, fftTime):
        fft_tot     =  np.sum(fftValues)
        
        F50_Sum     = 0
        for i in fftValues:
            F50_Sum += i
            if ((F50_Sum / fft_tot) >= 0.5):
                F50_idx = np.where(fftValues == i)[0]
                F50 = fftTime[F50_idx]
                break
        return F50[0]
        
    def F95(fftValues, fftTime):
        fft_tot     =  np.sum(fftValues)
        
        F95_Sum     = 0
        for i in fftValues:
            F95_Sum += i
            if ((F95_Sum / fft_tot) >= 0.95):
                F95_idx = np.where(fftValues == i)[0]
                F95 = fftTime[F95_idx]
                break  
        return F95[0]
    
    def fft_tot(fftValues):
        fft_tot     =  np.sum(fftValues)
        return fft_tot
    
    def spectralCentroid(signal):
        fftValues  = signal
        fft_tot     =  np.sum(fftValues)
        normalized_spectrum = fftValues / fft_tot
        normalized_frequencies = np.linspace(0,1,len(fftValues))
        SpectralCentroid = np.sum(normalized_spectrum * normalized_frequencies)
        return SpectralCentroid
        
        
        
        
