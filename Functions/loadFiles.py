import os

import pandas as pd
import numpy as np

from visualise import Visualisation

class loadCsv():
    def __init__(self, owd, position,  testType, plotje, resample, subjn = None, making_sense = True, ): 
        '''
        This function is used to create an object of the sensor data that 
        contains the sample frequency, raw acceleration [m/s^2] and corrected 
        gyroscope ('rad/s'). This object will be further used in functions to 
        store variables. 
        The first 200 and last 200 samples are always skipped.
        The gyroscope is converted to rad/s.
        The gyroscope constant bias error is corrected using values determined in a 
        static test. To add a new calibration file go to: main_files/add_calibration
        Samplefrequenty is calculated based on the IMU timestamps
        Possibility to plot the raw acceleration adn gyroscope signal.
        '''
        if making_sense:
            if testType == 'Test':
                 testwd = owd + "/Data_makingsense/" + subjn
                 os.chdir(testwd) 
                 xls = pd.read_excel('Excel_logbestanden' + subjn + '.xlsx',        # Read the Excel file
                                     skiprows = 4)
                 num = xls.at[position,'Log OR']
                 if isinstance(num, str):                                           # Get the number from the excel file
                     if (len(num) > 5):
                         num = int(num[-2] + num[-1])
                     else:
                         num = int(num[-1])                                                    
                 fileName = 'log' + str(num).zfill(3) + '.csv'                              # Select the correct LOG from excel               
    
                     
                 testwd = testwd + "/Test/Onderrug"                                 # Working directory
                 os.chdir(testwd) 
                 
            elif testType == 'Hertest':
                 testwd = owd + "/Data_makingsense/" + subjn
                 os.chdir(testwd) 
                 xls = pd.read_excel('Excel_logbestanden' + subjn + '.xlsx',        # Read the Excel file
                                     skiprows = 4)
                 num = xls.at[position,'Log OR']
                 if isinstance(num, str):
                     if (len(num) > 5):
                         num = int(num[-2] + num[-1])
                     else:
                         num = int(num[-1])
                 fileName = 'log' + str(num).zfill(3) + '.csv'                              # Select the correct LOG from excel               
                
                 testwd = testwd + "/Hertest/Onderrug"                              # Working directory
                 os.chdir(testwd) 
        else:
            testwd = owd + "/Data/"
            os.chdir(testwd) 
            fileName = position
            
        data  = pd.read_csv(fileName,                                           # Load the log file
                              header = 0,                       
                              names = ['T', 'ax', 'ay', 'az', 'gx', 'gy', 'gz'], 
                              skiprows = 9, 
                              sep = ',',
                              error_bad_lines = False
                              )       
        
        data.dropna(how = 'any',inplace = True)
        for i in data.columns[1:]:
            data[i] = pd.to_numeric(data[i], downcast = 'float')          
        
        serialnumber = pd.read_csv(fileName,nrows = 1).loc[0][0]         # Get sensor serial number to correct gyroscope bias
        os.chdir(owd)     
        
        if resample:                                                            # Resample              
            resampleFrequecy= 0.01                                 # Resample to 100 per second
            tmpsampleFreq = (1/( 10000/np.mean(np.diff(data.iloc[:,0])) ))
            tmptime= np.array(data['T'])
            tmptime = (tmptime - tmptime[0] ) /10000
            newTime = np.arange(0,round(len(tmptime) * tmpsampleFreq,2),resampleFrequecy) 
    
            lindx = []
            
            for i in newTime:
                idx = np.abs(i - tmptime).argmin()
                lindx.append(idx)
                
            self.gyroscope =  np.radians(np.array(data.iloc[lindx,4:7]))
            self.acceleration = np.array(data.iloc[lindx,1:4])
            self.sampleFreq = resampleFrequecy
        
        else:
            self.sampleFreq = (1/( 10000/np.mean(np.diff(data.iloc[:,0])) ))
            self.acceleration =  np.array(data.iloc[:,1:4])           
            self.gyroscope =  np.radians(np.array(data.iloc[:,4:7])) 

        try:
            calibwd = owd + '/calibration'                                     # Working directory
            os.chdir(calibwd)             
            gyorscopeErrorDF = pd.read_pickle('gyorscopeErrorDF.pkl')
            gyrEx, gyrEy, gyrEz = gyorscopeErrorDF.loc[serialnumber]         
            self.gyroscope -= gyrEx, gyrEy, gyrEz 
        except TypeError:
            print('Warning: Calibrate this sensor before using!')
        
        os.chdir(owd) 
        self.gyroscope = self.gyroscope[200:-200]
        self.acceleration = self.acceleration[200:-200]
                           
        if plotje: 
            Visualisation.plot1(self.acceleration, title = 'Raw acceleration signal', 
                     xlabel = 'Samples', ylabel = 'Acceleration [g]')
            Visualisation.plot1(self.gyroscope, title = 'Raw gyroscope signal', 
                                 xlabel = 'Samples', ylabel = 'Gyroscope [deg/s]')
            