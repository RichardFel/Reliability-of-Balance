'''
Created by R. Felius 27/08/2020 in collaboration with Hogeschool Utrecht,
Vrije universiteit Amsterdam, De Parkgraaf en de Hoogstraat Revalidatie.
Modified at 25/06/2021

This script is written to analyse data for the project: 
Making sense of sensor data for personalised healthcare.
This script can be used to analyse static postural balance.

The inputs are CSV files with 7 columns: Timestamp [0], IMU accelerometer [1,2,3] 
and gyroscope [4,5,6] data. See /Data for an example.

IMPORTANT:
- Set working directory
- Calculate gyroscope bias prior to measurement, see /Calibration/calibration.py

To calibrate new sensors 
from calibration import addCalibration
addCalibration.determineGyroscopeError(mainDirectory, verbose = True)    
'''


import numpy
from Functions.calcBalanceFeautres import calcFeaturesMakingSense
from Functions.calcICC import calculateICCMDC
from Functions.pythontolatex import meanStdtoLatex,iccmdctoLatex,mdcRawToLatex
from Functions.balansplot import plotSIT,plotStanding

rehabC = ('P','H')                                                              
testTypes = ('Test','Hertest')                                                  
nSubjects = 21                                                                   
tasks = numpy.array([('Zitten', 60,0),                                          
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


def main():
    calcFeaturesMakingSense(settings, measuringTwice = False, plotje = False, verbose = True )
    calculateICCMDC(measurement = 'FM')
    meanStdtoLatex(measurement = 'FM')
    iccmdctoLatex(measurement = 'FM')
    calcFeaturesMakingSense(settings, measuringTwice = True, plotje = False, verbose = True)     
    calculateICCMDC(measurement = 'AM')    
    meanStdtoLatex(measurement = 'AM')
    iccmdctoLatex(measurement = 'AM')
    mdcRawToLatex()
    plotSIT()
    plotStanding()
    
    
if __name__ == "__main__":
    main()
