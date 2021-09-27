'''
The input is a CSV file with Timestamp [0], IMU accelerometer [1,2,3] 
and gyroscope [4,5,6] data. 
The following variables are calculated:
    
* Time-Domain:
    - ACC/GYR/JERK mean, RMS
    - Distance, Path, mean velocity/Frequency, area
    - Cirkel Radius and ellipse Length/Width
    
* Frequency-domain:
    - Total power, 50%, 95%, centroidal frequency  
    
* Complexity:
   - Lyapunov exponent:  Short term divergence exponent
   - Entropy: ACC Sample- and approximateentropy


The raw acceleration signals in our study rhougly correspond to the following 
direction in the global axis.
Lowback sensor:
forward/backward:       acceleration[:,2]
left/right:             acceleration[:,1]
up/down:                acceleration[ ,0]

Literature is cited at the bottom.
'''

import unittest
import os
import sys

import numpy as np

mainDirectory = os.getcwd()
sys.path.append(str(mainDirectory + '/Functions'))
import saveResults 
import errors
from spatioTemporalFeatures import spatioTemporal
from frequencyFeatures import fastfourierTransform
from complexityFeatures import Complexity
from loadFiles import loadCsv     
from visualise import Visualisation
from proces import Processing


# Making sense
Making_sense = True
rehabC = ('P','H') # Set availible rehabcentres
testTypes = ('Test','Hertest') # Testtype
nSubjects = 1  # Set number of participants
tasks = np.array([('Zitten', 60,0),  # Condition name, time, number
                  ('Staan',60,1), 
                  ('Staan voeten samen', 60,3),
                  ('Staan ogen dicht', 30,5),
                  ('Staan op foam', 30, 7)
                  ])
    
settings = {'rehabC' : rehabC,
            'testTypes': testTypes,
            'nSubjects': nSubjects,
            'tasks': tasks
            }

def calcFeatures(settings, Making_sense, measuringTwice, plotje, verbose = None):
    if Making_sense == True:
        if measuringTwice == False:
            for task in settings['tasks']:                                          
                if verbose:
                    print('\n' + task[0] + '\n')        
                results =  saveResults.saveresults_balance()                                    
                results, lowBack = proces_data(rehabC = settings['rehabC'],         
                                               nSubjects= settings['nSubjects'],    
                                               testTypes = settings['testTypes'],   
                                               taskNum = task[2],                   
                                               time = task[1],                      
                                               results = results,                   
                                               trial = 0,                         
                                               plotje = plotje   ,
                                               verbose = verbose
                                               )       
                try:
                    os.chdir(mainDirectory + '/Results/Single measurement')
                    saveAs = 'FM_' + str(task[0]) + '.xlsx'
                    results.to_excel(saveAs)   
                    os.chdir(mainDirectory)
                    if verbose:
                        print('Results saved')
                except IndexError:
                    if verbose:
                        print('Save Error: No data in the results dataframe')
                    
        else:
            for task in settings['tasks'][1:]:  
                if verbose:
                    print('\n' + task[0] + '\n')                                         
                results =  saveResults.saveresults_balance()                                      
                for j in range(2):                                                  
                    taskNum = int(task[2]) + j
                    results, lowBack = proces_data(rehabC = settings['rehabC'],        
                                                   nSubjects= settings['nSubjects'],   
                                                   testTypes = settings['testTypes'],  
                                                   taskNum = taskNum,              
                                                   time = task[1],                 
                                                   results = results,               
                                                   trial = j,                       
                                                   plotje = plotje,
                                                   verbose = verbose
                                                   )      
                try:
                    os.chdir(mainDirectory + '/Results/Averaged measurements')
                    saveAs = 'AM_' + task[0] + '.xlsx'
                    results.to_excel(saveAs)    
                    os.chdir(mainDirectory)
                    if verbose:
                        print('Results saved')
                except IndexError:
                    if verbose:
                        print('Save Error: No data in the results dataframe')                             
    else:
        data_dir = mainDirectory + '/Data'
        files = os.listdir(data_dir)
        results =  saveResults.saveresults_balance()  
        for file in files:
            split = file.split(' ')
            subject = split[0]
            testType = file
            trial = 0
  
            try:         
                lowBack = read_data(locInExcel = file,
                                    testType = file,
                                    subject =  subject,            
                                    time = 60, 
                                    plotje = False, 
                                    verbose = False,
                                    making_sense = False
                                    )
                
                lowBack = calculate_feautres(lowBack, 
                                             plotje, 
                                             verbose
                                             )   
    

                results = saveResults.updatedataframe_balance(results,      
                                                              subject, 
                                                              testType,
                                                              trial,
                                                              lowBack
                                                              )
            except:  
                if verbose:                                                   
                        print('Subject: ', subject, 'Not included' + '\n') 


        os.chdir(mainDirectory + '/Results/Michiel')
        saveAs = 'Onstabiel_zitten.xlsx'
        results.to_excel(saveAs)    
        os.chdir(mainDirectory)
        
def proces_data(rehabC, nSubjects, testTypes, taskNum, time, results, 
                trial, plotje, verbose):
    
    for RevC in rehabC:                                                         
        for nSubject in range(1,nSubjects+1):                                    
            subject = 'S' + str(nSubject).zfill(3) + RevC 
            for testType in testTypes:                                          
                locInExcel = int(taskNum)
                if testType == 'Hertest':
                    locInExcel += 19
                if verbose:
                    print('\n subject: ', subject, '   test type: ', testType )
                
                try:         
                    lowBack = read_data(locInExcel,
                                        testType,
                                        subject,            
                                        time, 
                                        plotje, 
                                        verbose
                                        )
                    
                    lowBack = calculate_feautres(lowBack, 
                                                 plotje, 
                                                 verbose
                                                 )         

                    results = saveResults.updatedataframe_balance(results,      
                                                                  subject, 
                                                                  testType,
                                                                  trial,
                                                                  lowBack
                                                                  )
                except:  
                    if verbose:                                                   
                            print('Subject: ', subject, 'Not included' + '\n')
    return results, lowBack

                
def read_data(locInExcel, testType, subject, time, plotje, verbose, making_sense):  
    
    try:
        lowBack            = loadCsv(owd = mainDirectory,
                                     position = locInExcel,  
                                     testType = testType,
                                     plotje = plotje,
                                     resample = True,
                                     subjn = subject,
                                     making_sense = making_sense
                                     )
    except (FileNotFoundError, ValueError):
        if verbose:
            print('Input Error: No input file found')
     
    # Checks if signal length is as expected

    try:
        if  time == '60':
            if len(lowBack.acceleration) < 5600:                                
                raise errors.inputTooShortError
            elif len(lowBack.acceleration) > 7500:                             
                raise errors.inputTooLongError
            else:
                lowBack.acceleration = lowBack.acceleration[0:5600]             
                lowBack.gyroscope = lowBack.gyroscope[0:5600]
                if verbose:
                    print('Checkpoint 1: Load succesfull')
        else:
            if len(lowBack.acceleration) < 2600:                                
                raise errors.inputTooShortError
            elif len(lowBack.acceleration) > 6500:                              
                print(len(lowBack.acceleration))
                raise errors.inputTooLongError
            else:
                lowBack.acceleration = lowBack.acceleration[0:2600]             
                lowBack.gyroscope = lowBack.gyroscope[0:2600]
                if verbose:
                    print('Checkpoint 1: Load succesfull')
           
            return lowBack
    
    except errors.inputTooShortError:
        if verbose:
            print('Input Length Error: Input file too short')
        raise Exception
    except errors.inputTooLongError:
        if verbose:
            print('Input Length Error: Input file too long')
        raise Exception        


def calculate_feautres(lowBack, plotje, verbose, area = None):             
    # Pre rotation: acc = [VT, ML, AP], Post rotation: acc = [AP, ML, VT]
    lowBack.rotAcc, lowBack.rotGyro = Processing.bruijn_rotation(lowBack,   
                                                                 plotje = plotje) 
    # Third order butterworth highpass 0.4 Hz 
    lowBack.filtAcc = Processing.filt_high(lowBack.rotAcc,  
                                                    lowBack.sampleFreq,   
                                                    cutoff = 0.4, 
                                                    order = 3,
                                                    n_input = 3)  
    if verbose:
        print('Checkpoint 2: Signal rotated and filtered')

    if plotje:
        Visualisation.plot1(lowBack.filtAcc, 
                            'Rotated and filtered acceleration', 
                            ylim = False)    
    
    # Spatiotemporal features
    lowBack.accMag          = spatioTemporal.magnitude(lowBack.filtAcc) 
    lowBack.accMagMean      = np.mean(lowBack.accMag)     
                      
    lowBack.jerkAP          = spatioTemporal.jerk(lowBack.filtAcc[:,0], 
                                                  lowBack.sampleFreq)               
    lowBack.jerkML          = spatioTemporal.jerk(lowBack.filtAcc[:,1], 
                                                  lowBack.sampleFreq)                   
    lowBack.jerktot         = spatioTemporal.Jerktot(lowBack.filtAcc, 
                                                  lowBack.sampleFreq)                     
     
    lowBack.jerkAPrms       = spatioTemporal.RMS(lowBack.jerkAP)
    lowBack.jerkAPrange     = spatioTemporal.RANGE(lowBack.jerkAP)
    
    lowBack.jerkMLrms       = spatioTemporal.RMS(lowBack.jerkML)
    lowBack.jerkMLrange     = spatioTemporal.RANGE(lowBack.jerkML)
    
    lowBack.accAPrms        = spatioTemporal.RMS(lowBack.filtAcc[:,0])
    lowBack.accAPrange      = spatioTemporal.RANGE(lowBack.filtAcc[:,0])
    
    lowBack.accMLrms        = spatioTemporal.RMS(lowBack.filtAcc[:,1])
    lowBack.accMLrange      = spatioTemporal.RANGE(lowBack.filtAcc[:,1])
    
    lowBack.gyrAPrms        = spatioTemporal.RMS(lowBack.rotGyro[:,0])
    lowBack.gyrAPrange      = spatioTemporal.RANGE(lowBack.rotGyro[:,0])
    
    lowBack.gyrMLrms        = spatioTemporal.RMS(lowBack.rotGyro[:,1])
    lowBack.gyrMLrange      = spatioTemporal.RANGE(lowBack.rotGyro[:,1])
                                            
    lowBack.dist            = spatioTemporal.dist(lowBack.filtAcc) 
    lowBack.path            = spatioTemporal.path(lowBack.filtAcc)   
    lowBack.disp            = spatioTemporal.displacement(lowBack.filtAcc)   
    lowBack.meanVelocity    = spatioTemporal.meanVelocity(lowBack.filtAcc, 
                                                          lowBack.sampleFreq)  
    lowBack.meanFrequency   = spatioTemporal.meanfreq(lowBack)
    lowBack.area            = spatioTemporal.area(lowBack.jerktot)
    
    lowBack.circleArea = spatioTemporal.within_cirkel(lowBack.filtAcc, 
                                                       percentage = 95,         
                                                       plotje = plotje,
                                                       circarea = 0.001)
    
    lowBack.ellipseArea  = spatioTemporal.within_ellipse(lowBack.filtAcc, 
                                                           percentage = 90,   
                                                           plotje = plotje,
                                                           ellipl = 0.002,
                                                           ellipw = 0.001)
    
    
    # Frequency features
    lowBack.accFT       = np.array(lowBack.filtAcc)
    lowBack.fftsignalML = fastfourierTransform(signal = lowBack.accFT[:,1],
                                               sampleFreq = lowBack.sampleFreq,
                                               lineartaper = None,
                                               plotje = plotje,
                                               window = True)  

    lowBack.fftsignalML.F50 = fastfourierTransform.F50(lowBack.fftsignalML.fftValues,
                                                       lowBack.fftsignalML.fftTime
                                                       )
    
    lowBack.fftsignalML.F95 = fastfourierTransform.F95(lowBack.fftsignalML.fftValues,
                                                       lowBack.fftsignalML.fftTime
                                                       )
    
    lowBack.fftsignalML.fft_tot = fastfourierTransform.fft_tot(lowBack.fftsignalML.fftValues)
    lowBack.fftsignalML.SpectralCentroid = fastfourierTransform.spectralCentroid(lowBack.fftsignalML.fftValues)
    
    lowBack.fftsignalAP = fastfourierTransform(signal = lowBack.accFT[:,0],
                                               sampleFreq = lowBack.sampleFreq,
                                               lineartaper = None,
                                               plotje = plotje,
                                               window = True)  
    

    lowBack.fftsignalAP.F50 = fastfourierTransform.F50(lowBack.fftsignalAP.fftValues,
                                                       lowBack.fftsignalAP.fftTime
                                                       )
    
    lowBack.fftsignalAP.F95 = fastfourierTransform.F95(lowBack.fftsignalAP.fftValues,
                                                       lowBack.fftsignalAP.fftTime
                                                       )
    
    lowBack.fftsignalAP.fft_tot = fastfourierTransform.fft_tot(lowBack.fftsignalAP.fftValues)
    lowBack.fftsignalAP.SpectralCentroid = fastfourierTransform.spectralCentroid(lowBack.fftsignalAP.fftValues)
    


    # Complexity features 
    lowBack.stateAP = Complexity.statespace(signal = np.vstack(lowBack.filtAcc[:,0]), 
                                            ndim = 5, 
                                            delay = 10
                                            )
    
    lowBack.stateML = Complexity.statespace(signal = np.vstack(lowBack.filtAcc[:,1]), 
                                            ndim = 5, 
                                            delay = 10
                                            )
    
    lowBack.divAP,lowBack.ldeAP = Complexity.rosenstein(lowBack,          
                                                        state = lowBack.stateAP,
                                                        period = 1, 
                                                        ws = 0.5, 
                                                        nnbs = 5, 
                                                        plot = plotje
                                                        )
    
    lowBack.divML,lowBack.ldeML = Complexity.rosenstein(lowBack,          
                                                        state = lowBack.stateML,
                                                        period = 1, 
                                                        ws = 0.5, 
                                                        nnbs = 5, 
                                                        plot = plotje
                                                        )
    
    lowBack.approxEntropyAP = Complexity.aproximateEntropy(m = 3,          
                                                           r = np.std(lowBack.filtAcc[:,0]  * 0.3), 
                                                           signal = lowBack.filtAcc[:,0]
                                                           )
    
    lowBack.approxEntropyML = Complexity.aproximateEntropy(m = 3,          
                                                           r = np.std(lowBack.filtAcc[:,1]  * 0.3), 
                                                           signal = lowBack.filtAcc[:,1]
                                                           )
    
    lowBack.sampleEntropyAP = Complexity.sampleEntropy(m = 3,              
                                                       r = np.std(lowBack.filtAcc[:,0]  * 0.3) , 
                                                       signal = lowBack.filtAcc[:,0] 
                                                       )
    
    lowBack.sampleEntropyML = Complexity.sampleEntropy(m = 3,              
                                                       r = np.std(lowBack.filtAcc[:,1] * 0.3),  
                                                       signal = lowBack.filtAcc[:,1] 
                                                       )
    if verbose:
        print('Checkpoint 3: All features succesfully computed')

    return lowBack


class Testfeatures(unittest.TestCase):
    def test_complete(self) :
        nSubject = 1 
        rehabC = ('P')
        trial = 0
        tasks = np.array([('Zitten', 60, 0)])     
#        tasks = np.array([('Foam', 30, 7)])     

        subject = 'S' + str(nSubject).zfill(3) + rehabC[0] 
        testType = 'Test'
        locInExcel = int(tasks[0,2])
        lowBack = read_data(locInExcel = locInExcel,testType = testType, subject = subject, time = tasks[0,1], plotje = True)       
        lowBack = calculate_feautres(lowBack, plotje = True)
        results =  saveResults.saveresults_balance()
        results = saveResults.updatedataframe_balance(results, 
                          subject, 
                          testType,
                          trial,
                          lowBack)
        
        
        print("ML RMS: " + str(lowBack.accMLrms))
        print("ML FFT TOT: " + str(lowBack.fftsignalML.fft_tot))       
        
        
    def test_Tooshort(self):
        nSubject = 2 
        rehabC = ('P')
        tasks = np.array([('Zitten', 60, 0)])     
        subject = 'S' + str(nSubject).zfill(3) + rehabC[0] 
        testType = 'Test'
        locInExcel = int(tasks[0,2])
        try:
            read_data(locInExcel = locInExcel,testType = testType, subject = subject, time = tasks[0,1], plotje = False)           
        except Exception:
            pass
            
    def test_noFile(self):
        nSubject = 5 
        rehabC = ('P')
        tasks = np.array([('Staan',60,1)])
        subject = 'S' + str(nSubject).zfill(3) + rehabC[0] 
        testType = 'Test'
        locInExcel = int(tasks[0,2])
        try:
            read_data(locInExcel = locInExcel,testType = testType, subject = subject, time = tasks[0,1], plotje = False)           
        except Exception:
            pass          
            
    def test_process(self):
        class Sensor:
            def __init__(self, sampleFreq, acceleration, gyroscope):
                self.sampleFreq = sampleFreq
                self.acceleration = acceleration
                self.gyroscope = gyroscope
                
        time = np.arange(0,10,0.01)
        Freq1 = 1
        Freq2 = 2
        amplitude1 = amplitude3 = np.sin(2 *np.pi*Freq1 * time)
        amplitude2 = np.sin(2 *np.pi*Freq2 * time)
        #noise = np.random.normal(0,1,10000)
        acceleration =  gyroscope = np.zeros((len(time),3))
        acceleration[:,0] = gyroscope[:,0] = amplitude1
        acceleration[:,1] = gyroscope[:,1] = amplitude2
        acceleration[:,2] = gyroscope[:,2] = amplitude3
        lowBack = Sensor(0.01, acceleration, gyroscope)
        #        Visualisation.plot1(acceleration)
        lowBack = calculate_feautres(lowBack, plotje = False, area = False)
        #        print("AP RMS: " + str(lowBack.accAPrms))
        #        print("AP FFT TOT: " + str(lowBack.fftsignalAP.fft_tot))

        '''
        nTests = 8
        import matplotlib.pyplot as plt
        fig1, ax2 = plt.subplots(nTests)
        # Test Frequency & RMS 
        for i in range(0,nTests,1):
            amplitude3 = amplitude3 + np.random.normal(0,0.1 * i,1000)
            ax2[i].plot(amplitude3) 
            lowBack.acceleration[:,2] = amplitude3
            lowBack = calculate_feautres(lowBack, plotje = False, area = False)
            print("PLot: " + str(i))
        '''    
  
       
if __name__ == "__main__":
     calcFeatures(settings,Making_sense, measuringTwice = False, plotje = False, 
                   verbose = True
                   )       
     calcFeatures(settings, Making_sense, measuringTwice = True, plotje = False, 
                   verbose = True
                   )      
    
    
'''
Literature:  
    Bruijn, S., Bregman, D., Meijer, O., Beek, P., & Van Dieen, J. (2011, 08).
Maximum lyapunov exponents as predictors of global gait stability: A
modelling approach. Medical engineering & physics, 34, 428-36. doi:
10.1016/j.medengphy.2011.07.024

    Helbostad, J., Askim, T., & Moe-Nilssen, R. (2004, 01). Short-term repeatability
of body sway during quiet standing in people with hemiparesis and in frail
older adults 1 1 no commercial party having a direct financial interest in
the results of the research supporting this article has or will confer a benefit
on the author(s) or on any organization with which the author(s) is/are
associated. Archives of Physical  
    
    Ghislieri, M., Gastaldi, L., Pastorelli, S., Tadano, S., & Agostini, V. (2019, 09).
Wearable inertial sensors to assess standing balance: A systematic review.
Sensors, 19, 4075. doi: 10.3390/s19194075

    Mancini, M., Salarian, A., Carlson-Kuhta, P., Zampieri, C., King, L., Chiari, L.,
& Horak, F. (2012, 08). Isway: A sensitive, valid and reliable measure of
postural control. Journal of neuroengineering and rehabilitation, 9, 59. doi:
10.1186/1743-0003-9-59

'''

