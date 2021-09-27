import numpy as np
from scipy import signal
from visualise import Visualisation


class Processing: 
    def filt_band(input_signal,  samplefreq, cutoff_h,cutoff_l , order =1, n_input = 1 ):
        '''
        Butterworth bandpass filter
        '''
        filtacceleration = np.zeros((len(input_signal),n_input))
        try:
            for k in range(0,n_input):                                                 
                b, a = signal.butter(order, (2*cutoff_h)/(1/samplefreq), 'highpass');
                filtacceleration[:,k] = signal.filtfilt(b,a, input_signal[:,k])
                b, a = signal.butter(order, (2*cutoff_l)/(1/samplefreq), 'lowpass');
                filtacceleration[:,k] = signal.filtfilt(b,a, input_signal[:,k])
            return filtacceleration
        except IndexError:
            filtacceleration = np.zeros(len(input_signal))
            for k in range(0,n_input):                                                 
                b, a = signal.butter(order, (2*cutoff_h)/(1/samplefreq), 'highpass');
                filtacceleration[:] = signal.filtfilt(b,a, input_signal[:])
                b, a = signal.butter(order, (2*cutoff_l)/(1/samplefreq), 'lowpass');
                filtacceleration[:] = signal.filtfilt(b,a, input_signal[:])
            return filtacceleration
    
    def filt_high(input_signal, samplefreq, cutoff, order =1, n_input = 1):
        '''
        Butterworth highpass filter
        '''                              
        filtacceleration = np.zeros((len(input_signal),n_input))
        try: 
            for k in range(0,n_input):
                b, a = signal.butter(order, (2*cutoff)/(1/samplefreq), 'highpass');
                filtacceleration[:,k] = signal.filtfilt(b,a, input_signal[:,k])
            return filtacceleration
        except IndexError: 
             for k in range(0,n_input):
                b, a = signal.butter(order, (2*cutoff)/(1/samplefreq), 'highpass');
                filtacceleration[:,k] = signal.filtfilt(b,a, input_signal[:])
             return filtacceleration
         
    def filt_low(input_signal, samplefreq, cutoff, order = 1,  n_input = 1): 
        '''
        Butterworth lowpass filter
        '''                                 
        filtacceleration = np.zeros((len(input_signal),n_input))
        try: 
            for k in range(0,n_input):
                b, a = signal.butter(order, (2*cutoff)/(1/samplefreq), 'lowpass');
                filtacceleration[:,k] = signal.filtfilt(b,a, input_signal[:,k])
            return filtacceleration
        except IndexError: 
            for k in range(0,n_input):
                b, a = signal.butter(order, (2*cutoff)/(1/samplefreq), 'lowpass');
                filtacceleration[:,k] = signal.filtfilt(b,a, input_signal[:])
            return filtacceleration


    def localToGlobal(lowBack, stationary = False, plotje = None):
            '''
             Input: 
             3D-acceleration time series with intended orientation:
             Low back sensor:
             forward/backward:       acceleration[:,2]
             left/right:             acceleration[:,1]
             up/down:                acceleration[ ,0]    
            
             Output: 
             
             RotationMatrixT: Transpose of rotation matrix used for realignment 
             Define VT direction (RVT) as direction of mean acceleration
             
             Theory
             The mean of AP and ML will with a large by default be an estimate of the
             gravity component in the signal.
             AP: positive direction forward, positive rotation upward
             VT: positive direction upward
             ML: positive direction right, positive rotation upward
             
             Move2data sensor on lowerback:
            Positive is backward
            positive is upward
            positive is left
    
             Moe-Nilssen, R. (1998). A new method for evaluating motor control in gait under 
             real-life environmental conditions. Part 1: The instrument. Clinical Biomechanics, 
             13(4-5), 320–327. doi:10.1016/s0268-0033(98)00089-8 
            '''
            if stationary:
                stationary      = np.concatenate((lowBack.startEnd))
                APaccel         = lowBack.acceleration[stationary,2]
                MLaccel         = lowBack.acceleration[stationary,1]
            else:
                APaccel         = lowBack.acceleration[:,2]
                MLaccel         = lowBack.acceleration[:,1]      
                
            APbar           = np.mean(APaccel)
            MLbar           = np.mean(MLaccel)
            
            sin_theta_AP    = APbar
            cos_theta_AP    = np.sqrt(1-(np.power(APbar,2)))
            sin_theta_ML    = MLbar
            cos_theta_ML    = np.sqrt(1-(np.power(MLbar,2)))
            
            APraw           =lowBack.acceleration[:,2]
            MLraw           =lowBack.acceleration[:,1]
            VTraw           =lowBack.acceleration[:,0]
    
            AP              =(APraw*cos_theta_AP)-(VTraw*sin_theta_AP)
            VT1             =(APraw*sin_theta_AP)+(VTraw*cos_theta_AP)
            ML              =(MLraw*cos_theta_ML)-(VT1*sin_theta_ML)
            VT              =(MLraw*sin_theta_ML)+(VT1*cos_theta_ML)-1        
            
            trueAcc         = np.array((VT, ML, AP)).transpose()
            
            if plotje:
                Visualisation.plot1(trueAcc, 'Acceleration VT, ML, AP', 'Samples', 'Acceleration [G]')
            
            return trueAcc   
        
        
    def bruijn_rotation(lowBack, plotje = None):
        '''
         Input: 
         3D-acceleration/gyroscope time series with intended orientation:
         Low back sensor:
         forward/backward:       acceleration[:,2]
         left/right:             acceleration[:,1]
         up/down:                acceleration[ ,0]    
        
         Output: 
         Acceleration and gyroscope signal rotated to global axis
        '''
        
        gyroscope = lowBack.gyroscope
        acceleration = lowBack.acceleration
        
        meanAcceleration = np.mean(acceleration,axis = 0)
        
        x_tmp=np.array([0, 0, 1])
        y=np.cross(meanAcceleration,x_tmp)
        x=np.cross(y,meanAcceleration)
           
        normx=x/np.linalg.norm(x)
        normy=y/np.linalg.norm(y)
        normz= meanAcceleration / np.linalg.norm(meanAcceleration)
         
        R=np.array((normx.transpose(), normy.transpose(), normz.transpose()))
         
        accRotated=(R.transpose().dot(acceleration.transpose())).transpose()
        gyrRotated =(R.transpose().dot(gyroscope.transpose())).transpose()
        
        
        if plotje:
            Visualisation.plot1(accRotated, 'Acceleration VT, ML, AP', 'Samples', 'Acceleration [G]')
            Visualisation.plot1(gyrRotated, 'Gyroscope VT, ML, AP', 'Samples', 'Angular velocity [deg/s]')
            
        return accRotated, gyrRotated
        