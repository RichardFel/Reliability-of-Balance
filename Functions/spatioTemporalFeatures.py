import numpy as np
import matplotlib.pyplot as plt
from scipy import  integrate

class spatioTemporal:  
    def RMS(signal): # Root mean square
        RMS = np.sqrt(np.mean(signal**2))
        return RMS
    
    def RMSE(signal): # Root mean square error
        RMSE = np.sqrt((sum((np.mean(signal) - signal)**2)/(len(signal)-1)))                                                  
        return RMSE
    
    def magnitude(signal):  # magnitude
        magnitude = np.sqrt(np.sum(signal * signal, axis = 1))                                 
        return magnitude
     
    def STD(signal): # standard deviation                                              
        std = (np.std(signal))
        return std
    
    def RANGE(signal):   # Range
        Range = np.max(signal) - np.min(signal)  
        return Range
                      
    def jerk(filtAcc, sampleFreq): # Jerk
        jerk = np.gradient(filtAcc, sampleFreq)
        return jerk
    
    def Jerktot(filtAcc, sampleFreq): # Jerk combined
        ML = filtAcc[:,1]
        AP = filtAcc[:,0]
        
        jerkAP = np.power(np.gradient(AP, sampleFreq),2)
        jerkML = np.power(np.gradient(ML, sampleFreq),2)
        jerkAP_ML = jerkAP + jerkML
        jerk   = 0.5 * integrate.cumtrapz(jerkAP_ML,dx = sampleFreq)
        return jerk
    
    
    def meanVelocity(filtAcc, sampleFreq): # Mean velocity of AP and ML
        velocityAP = integrate.cumulative_trapezoid(filtAcc[:,0], 
                                        dx= sampleFreq, axis = 0)
        velocityML = integrate.cumulative_trapezoid(filtAcc[:,1], 
                                        dx= sampleFreq, axis = 0)
        velocity = np.mean(np.hypot(velocityAP,velocityML))
        return velocity 
      
    def dist(filtAcc):  # Mean distance from centre
        acceleration = filtAcc - np.mean(filtAcc, axis = 0)  
        dist = np.mean(np.abs(acceleration[:,1]) + np.abs(acceleration[:,2]) )    
        return dist

    def displacement(filtAcc): #  Displacement
        AP = filtAcc[:,0] 
        ML = filtAcc[:,1]
        displacement =  np.sum(np.abs(np.diff(AP))) + np.sum(np.abs(np.diff(ML)))
        return displacement

    
    def path(filtAcc):  # Sway path of Acceleration
        accelerationAP = filtAcc[:,0], 
        accelerationML = filtAcc[:,1],  
        path = np.sum(np.hypot(accelerationAP,accelerationML))
        return path
    
    def meanfreq(lowBack): # Number of seconds to cover a trajectory
        meanFrequency = lowBack.path / (2* np.pi * lowBack.dist * len(lowBack.filtAcc))
        return meanFrequency
    
    def area(jerk): # Sway area per unit time
        area = np.max(jerk) / len(jerk)
        return area
    
    def within_cirkel(filtAcc, percentage = 95, plotje = None, circref = None, 
                      test = "balance", circarea = None):
        '''
        Draw a cirkel around min n% of the datapoints.
        '''
        
        AP = filtAcc[:,0] - np.mean(filtAcc[:,0])
        ML = filtAcc[:,1] - np.mean(filtAcc[:,1])
        pythagoras = np.hypot(AP, ML)# Distance of every sample from the absolute zero
        check = False
        cirkel = circarea
        increase = circarea
        while check == False:
            n = np.where(pythagoras < cirkel)[0]
            if ((len(n) / len(pythagoras)) >= (percentage / 100)):
                check = True
            else:
                cirkel += increase
                
        cirkelArea = np.power(cirkel, 2) * np.pi 
        if plotje:
            fig, ax = plt.subplots()
            a_circle = plt.Circle((0,0),  cirkel, fill=False, label = 'Circle participant')
            ax.add_artist(a_circle)
            plt.plot(AP, ML, alpha = 0.25)
            ax.set_aspect('equal')
            ax.set(xlim=(-(cirkel * 2), (cirkel * 2)), ylim=(-(cirkel * 2), (cirkel * 2)))
            ax.set_title(('Cirkel around ML and AP of: ' + test))
            ax.set_xlabel('AP')
            ax.set_ylabel('ML')
            ax.legend([a_circle], ['Circle participant'])
            if circref: 
                ref1 = np.sqrt((circref[0] / np.pi))
                ref2 = np.sqrt((circref[1] / np.pi))
                
                if ((cirkelArea < circref[0]) or (cirkelArea < circref[1])):
                    ax.set(xlim=(-(ref1 * 2), (ref1 * 2)), ylim=(-(ref1 * 2), (ref1 * 2)))
                               
                circleStroke = plt.Circle((0,0),  ref1, fill=False, color='r', 
                                          label = 'reference stroke')
                ax.add_artist(circleStroke)            
                circleHealthy = plt.Circle((0,0),  ref2, fill=False, color='blue',
                                           label = 'reference healthy')
                ax.add_artist(circleHealthy)         
                ax.legend([a_circle, circleStroke, circleHealthy], ['Circle participant',
                          'Circle Stroke',
                          'Circle Healthy'])
        
        cirkelArea = np.power(cirkel, 2) * np.pi 
        return cirkelArea
    
    def within_ellipse(filtAcc, percentage = 95, plotje = None, ellipseref = None, 
                       test = "Balance", ellipl = None, ellipw = None):
        from matplotlib.patches import Ellipse
        '''
        Draw a ellipse around min n% of the datapoints.
        '''
        
        AP = filtAcc[:,0] - np.mean(filtAcc[:,0])
        ML = filtAcc[:,1] - np.mean(filtAcc[:,1])
        ap = np.array([AP]).transpose()
        ml = np.array([ML]).transpose()
        points = np.concatenate((ap,ml), axis = 1)
        check = False
        
        tmpWidth = ellipl
        increasel = ellipl
        tmpHeight = ellipw
        increasew = ellipw
        while check == False:
            for rotAngle in range(0,180):
                ellipse = Ellipse(xy =(0, 0), 
                                  width = tmpWidth, 
                                  height = tmpHeight, 
                                  angle = rotAngle, 
                                  fill = True)
                
                pointInEllipse = len(np.where(ellipse.contains_points(points) == True)[0])
                if (pointInEllipse / len(AP) * 100) >= percentage:
                    check = True
                    break
            tmpWidth += increasel
            tmpHeight += increasew
              
                 
        if plotje:
            fig, ax = plt.subplots()
            newellipse = Ellipse(xy =(0, 0), 
                                  width = ellipse.width, 
                                  height = ellipse.height, 
                                  angle = ellipse.angle, 
                                  fill = False, 
                                  label = 'participant')
            ax.add_patch(newellipse)
            plt.plot(AP, ML, alpha = 0.25)
            ax.set_aspect('equal')
            ax.set(xlim=(-(ellipse.width * 2), (ellipse.width * 2)), ylim=(-(ellipse.height * 2), (ellipse.height * 2)))
            ax.set_xlabel('AP')
            ax.set_ylabel('ML')
            ax.set_title(('Ellipse around ML and AP of: ' + test))
    
            if ellipseref:
                elHealthyW = (((ellipseref[1] / np.pi) / 3) * 2)
                elHealthyH = (((ellipseref[1] / np.pi) / 3) * 1)
                elhealth = Ellipse(xy =(0, 0), 
                          width = elHealthyW,
                          height = elHealthyH,
                          angle = ellipse.angle, 
                          fill = False,
                          color='r', 
                          label = 'participant')
                ax.add_patch(elhealth)
                
                elStrokeW = (((ellipseref[0] / np.pi) / 3) * 2)
                elStrokeH = (((ellipseref[0] / np.pi) / 3) * 1)
                elstroke = Ellipse(xy =(0, 0), 
                                  width = elStrokeW, 
                                  height = elStrokeH, 
                                  angle = ellipse.angle, 
                                  fill = False,
                                  color='blue', 
                                  label = 'participant')
                ax.add_patch(elstroke)
                ax.legend([newellipse, elstroke, elhealth], 
                          ['ellipse participant','ellipse Stroke', 'ellipse Healthy'])
    
    
            
        ellipseArea = (ellipse.width * ellipse.height) * np.pi
        return ellipseArea
    
              

        