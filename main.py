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

import numpy
from Functions.calcBalanceFeautres import calcFeatures
                                          
testTypes = ('Test','Hertest')                                                 
nSubjects = 0                                                                   
tasks = numpy.array([('Test', 60,0)])  

settings = {'testTypes': testTypes,
            'tasks': tasks
            }


def main():
    calcFeatures(settings, plotje = False, verbose = True )

if __name__ == "__main__":
    main()
