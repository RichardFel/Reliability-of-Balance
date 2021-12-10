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

import os
import numpy as np

mainDirectory = os.getcwd()
import Functions.saveResults as saveResults
import Functions.errors as errors
from Functions.spatioTemporalFeatures import spatioTemporal
from Functions.frequencyFeatures import fastfourierTransform
from Functions.complexityFeatures import Complexity
from Functions.loadFiles import loadCsv, loadCsv_MakingSense     
from Functions.visualise import Visualisation
from Functions.proces import Processing

def calcFeatures(settings, plotje, verbose = None):
    data_dir = mainDirectory + '/Data'
    files = os.listdir(data_dir)
    results =  saveResults.saveresults_balance()  
    for file in files:
        split = file.split(' ')
        subject = split[0]
        if subject == '.DS_Store' :
            continue
        testType = file
        trial = 0
        print(f'\n Analysing subject {subject} \n')
        try:         
            lowBack = read_data(locInExcel = file,
                                testType = file,
                                subject =  subject,            
                                time = 60, 
                                plotje = False, 
                                verbose = False,
                                makingSense = False
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
        except Exception as e: 
                if verbose:                                                   
                    print('Subject: ', subject, 'Not included' + '\n')
                print(e)


    saveAs = 'Results/Onstabiel_zitten.xlsx'
    results.to_excel(saveAs)    

def calcFeaturesMakingSense(settings, measuringTwice, plotje, verbose = None):
    makingSense = True
    
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
                                           verbose = verbose,
                                           makingSense = makingSense
                                           )       
            try:
                saveAs = 'Results_MakingSense/Single measurement/' + 'FM_' + task[0] + '.xlsx'
                results.to_excel(saveAs)   
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
                                               verbose = verbose,
                                               makingSense = True
                                               )      
            try:
                saveAs = '/Results_MakingSense/Averaged measurements/' + 'AM_' + task[0] + '.xlsx'
                results.to_excel(saveAs)    
                if verbose:
                    print('Results saved')
            except IndexError:
                if verbose:
                    print('Save Error: No data in the results dataframe')                             

        
def proces_data(rehabC, nSubjects, testTypes, taskNum, time, results, 
                trial, plotje, verbose, makingSense):
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
                                        verbose,
                                        makingSense
                                        )
                    lowBack = calculate_feautres(lowBack, 
                                                 plotje, 
                                                 verbose
                                                 )         
                except Exception as e: 
                    if verbose:                                                   
                        print('Subject: ', subject, 'Not included' + '\n')
                    print(e)
                    continue
                results = saveResults.updatedataframe_balance(results,      
                                                              subject, 
                                                              testType,
                                                              trial,
                                                              lowBack
                                                              )

    return results, lowBack
    
         
def read_data(locInExcel, testType, subject, time, plotje, verbose, makingSense):  
    if makingSense:
        try:
            lowBack = loadCsv_MakingSense(owd = mainDirectory,
                                         position = locInExcel,  
                                         testType = testType,
                                         plotje = plotje,
                                         resample = True,
                                         subjn = subject
                                         )
        except (FileNotFoundError, ValueError):
            if verbose:
                print('Input Error: No input file found')
    else:
         try:
             lowBack = loadCsv(owd = mainDirectory,
                                 position = locInExcel,  
                                 testType = testType,
                                 plotje = plotje,
                                 resample = True,
                                 subjn = subject
                                 )
         except (FileNotFoundError, ValueError):
                if verbose:
                    print('Input Error: No input file found')


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
    except errors.inputTooShortError:
        if verbose:
            print('Input Length Error: Input file too short')
        raise Exception
    except errors.inputTooLongError:
        if verbose:
            print('Input Length Error: Input file too long')
        raise Exception        
    return lowBack

def calculate_feautres(lowBack, plotje, verbose, area = None):             
    # Pre rotation: acc = [VT, ML, AP], Post rotation: acc = [AP, ML, VT]
    lowBack.rotAcc, lowBack.rotGyro = Processing.bruijn_rotation(lowBack,plotje = plotje) 
    
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

