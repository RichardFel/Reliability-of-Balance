import pandas as pd
import numpy as np

def saveresults_balance():
    listofVariablesNames = listofvariables_balance()
    df = pd.DataFrame(columns = listofVariablesNames)

    return df


def updatedataframe_balance(dfresults, subject, testType, trial, lowBack):
    listofVariablesNames = listofvariables_balance()
    
    listofVariables = [
subject,
testType,
trial,

lowBack.accAPrange ,   
lowBack.accAPrms,

lowBack.accMLrange,                              
lowBack.accMLrms, 

lowBack.gyrAPrange,                                  
lowBack.gyrAPrms,

lowBack.gyrMLrange,
lowBack.gyrMLrms,                                 


lowBack.jerkAPrms ,
lowBack.jerkAPrange ,

lowBack.jerkMLrms ,
lowBack.jerkMLrange,


lowBack.accMagMean,
lowBack.meanFrequency, 
 
lowBack.dist,      
lowBack.disp,  
lowBack.meanVelocity, 
lowBack.path ,                
lowBack.area,
lowBack.circleArea ,
lowBack.ellipseArea,

lowBack.fftsignalAP.F50,
lowBack.fftsignalAP.F95, 
lowBack.fftsignalAP.fft_tot, 
lowBack.fftsignalAP.SpectralCentroid, 

lowBack.fftsignalML.F50,
lowBack.fftsignalML.F95, 
lowBack.fftsignalML.fft_tot, 
lowBack.fftsignalML.SpectralCentroid, 

lowBack.ldeAP ,
lowBack.approxEntropyAP,
lowBack.sampleEntropyAP,

lowBack.ldeML,
lowBack.approxEntropyML,
lowBack.sampleEntropyML
 ]

    tmpdf = pd.DataFrame(data = np.array([listofVariables]), 
                         columns = listofVariablesNames)
    
    dfresults = dfresults.append(tmpdf, ignore_index = True)
    return dfresults





def listofvariables_balance():
    listofVariablesNames = [
 'Subject number',
'testType',
'Trial',

'AP Acc Range' ,   
'AP Acc rms' ,

'ML Acc Range' ,   
'ML Acc rms' ,

'AP Gyr Range' ,   
'AP Gyr rms' ,

'ML Gyr Range' ,   
'ML Gyr rms' ,                          


'AP Jerk Range' ,   
'AP Jerk rms' ,

'ML Jerk Range' ,   
'ML Jerk rms' ,


'Mag Acc mean',
'mean Frequency',

'Distance',
'Displacement',
'Mean velocity', 
'Path',
'Area',
'Circle area',
'Ellipse area',

'AP 50% Freq',
'AP 95% Freq',
'Ap Total power',
'Ap Spectral centroid',

'ML 50% Freq',
'ML 95% Freq',
'ML Total power',
'ML Spectral centroid',

'LDE AP',
'ApproxE AP',
'SampleE AP', 

'LDE ML',
'ApproxE ML',
'SampleE ML'
    ] 
    return listofVariablesNames



