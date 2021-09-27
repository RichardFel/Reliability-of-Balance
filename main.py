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

'''


import os
import sys
import numpy

mainDirectory = os.getcwd()
sys.path.append(str(mainDirectory + '/calibration'))
sys.path.append(str(mainDirectory + '/Functions'))

from calibration import addCalibration
from calcBalanceFeautres import calcFeatures
from calcICC import calculateICCMDC
from pythontolatex import meanStdtoLatex,iccmdctoLatex,mdcRawToLatex
from balansplot import plotSIT,plotStanding

# Making sense structue
# Making_sense = True
#rehabC = ('P','H')                                                              # Set availible rehabcentres
#testTypes = ('Test','Hertest')                                                  # Testtype
#nSubjects = 21                                                                   # Set number of participants
#tasks = numpy.array([('Zitten', 60,0),                                          # Condition name, time, number
#                      ('Staan',60,1), 
#                      ('Staan voeten samen', 60,3),
#                      ('Staan ogen dicht', 30,5),
#                      ('Staan op foam', 30, 7)
#                      ])
Making_sense = False
rehabC = ('P')                                                              # Set availible rehabcentres
testTypes = ('Test','Hertest')                                                  # Testtype
nSubjects = 0                                                                   # Set number of participants
tasks = numpy.array([('Onstabiel zitten', 60,0)])  

settings = {'rehabC' : rehabC,
            'testTypes': testTypes,
            'nSubjects': nSubjects,
            'tasks': tasks
            }


def main():
    # Uncomment for making sense
    #    addCalibration.determineGyroscopeError(mainDirectory, verbose = True)    

    calcFeatures(settings, Making_sense, measuringTwice = False, plotje = False, 
                  verbose = True, )
    
    #    calculateICCMDC(measurement = 'FM')
    #    meanStdtoLatex(measurement = 'FM')
    #    iccmdctoLatex(measurement = 'FM')
    #    
    #    calcFeatures(settings, measuringTwice = True, plotje = False, 
    #                  verbose = True)     
    #    
    #    calculateICCMDC(measurement = 'AM')    
    #    meanStdtoLatex(measurement = 'AM')
    #    iccmdctoLatex(measurement = 'AM')
    #    
    #    mdcRawToLatex()
    #    
    #    plotSIT()
    #    plotStanding()
    
    
if __name__ == "__main__":
    main()
