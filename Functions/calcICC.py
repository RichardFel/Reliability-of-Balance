import os

import pandas as pd
import numpy as np
import pingouin as pg

mainDirectory = os.getcwd()


def calculateICCMDC(measurement):
    files = [measurement + '_Zitten',
             measurement + '_Staan', 
             measurement + '_Staan ogen dicht', 
             measurement + '_Staan op foam', 
             measurement + '_Staan voeten samen'
             ] 
    

    for filename in files:
        if measurement == 'FM':
            directory = mainDirectory + '/Results_MakingSense/Single measurement'
            os.chdir(directory)
            nFilesPP = 2
        elif measurement == 'AM':
            directory = mainDirectory + '/Results_MakingSense/Averaged measurements'
            os.chdir(directory)       
            nFilesPP = 4
        
        if filename == 'AM_Zitten':
            continue
        loadfile = filename + '.xlsx'
        xls = pd.read_excel(loadfile, index_col = 0)
        
        countValues = xls['Subject number'].value_counts()
        inComplete = countValues.loc[countValues != nFilesPP].index
        xls.drop(xls.loc[xls['Subject number'].isin(inComplete)].index, inplace = True)
        
        if measurement == 'FM':
            if filename == 'FM_Staan voeten samen':
                # 4,5 =  clonus : S006p
                xls.drop(xls.loc[xls['Subject number']== 'S006P'].index, inplace = True)
                # 13,14 = Stapjes: S014P       
                xls.drop(xls.loc[xls['Subject number'] == 'S014P'].index, inplace = True)
                
            elif filename == 'FM_Staan ogen dicht':
                # 5,6 = clonus: S006P
                xls.drop(xls.loc[xls['Subject number']== 'S006P'].index, inplace = True)
                # 13,14 = Stapjes: S014P       
                xls.drop(xls.loc[xls['Subject number'] == 'S014P'].index, inplace = True)
                
            elif filename == 'FM_Staan op foam':
                # 5,6 = clonus: S006P
                xls.drop(xls.loc[xls['Subject number']== 'S006P'].index, inplace = True)
                # 13,14 = Stapjes: S020P       
                xls.drop(xls.loc[xls['Subject number'] == 'S020P'].index, inplace = True)
                   
        elif measurement == 'AM':
            if filename == 'AM_staan voeten samen':
                # 5,6 = clonus: S006P
                xls.drop(xls.loc[xls['Subject number']== 'S006P'].index, inplace = True)
                # 13,14 = Stapjes: S014P       
                xls.drop(xls.loc[xls['Subject number'] == 'S014P'].index, inplace = True)
                
            elif filename == 'AM_staan ogen dicht':
                # 5,6 = clonus: S006P
                xls.drop(xls.loc[xls['Subject number']== 'S006P'].index, inplace = True)
                # 13,14 = Stapjes: S014P       
                xls.drop(xls.loc[xls['Subject number'] == 'S014P'].index, inplace = True)
            
            elif filename == 'AM_staan op foam':
                # 5,6 = clonus: S006P
                xls.drop(xls.loc[xls['Subject number']== 'S006P'].index, inplace = True)
                
                # 13,14 = Clonus: S020P       
                xls.drop(xls.loc[xls['Subject number'] == 'S020P'].index, inplace = True)
                # 13,14 = Clonus: S020P       
                
        results = pd.DataFrame(columns = xls.columns[3:]).astype(float)
        results = results.append(pd.Series(name='ICC', dtype = 'float64'))
        results = results.append(pd.Series(name='MDC', dtype = 'float64'))
        
        if measurement == 'AM':
            firstMeasurement = xls.loc[xls['Trial']== 0].reset_index(drop = True) 
            secondMeasurement = xls.loc[xls['Trial']== 1].reset_index(drop = True) 
            if len(firstMeasurement) == len(secondMeasurement):
                doubleDF = (firstMeasurement.iloc[:,3:] + secondMeasurement.iloc[:,3:])
                newDF = doubleDF.div(2)
                xls = firstMeasurement
                xls.iloc[:,3:] = newDF
            else:
                print(f'Something is wrong with calculation of: {filename}')
                break
            
        for variable in xls.columns[3:]:
            variableDF = xls[['Subject number', 'testType',  variable]]
            icc = pg.intraclass_corr(data=variableDF, targets='Subject number', raters = 'testType',
                                     ratings=variable).round(10)
            ICC = icc['ICC'].loc[1]
            CI = icc['CI95%'].loc[1]
            SEM = (np.std(variableDF.loc[:,variable]) * np.sqrt(1 - ICC))
            MDC = (1.96 * SEM * np.sqrt(2))
            SEM = SEM.round(3)
            ICC_CI = str(ICC.round(3))+ ' ['+ str(CI[0]) + ',' + str(CI[1]) + ']'    
            MDC_SEM = str(MDC.round(3))+ ' (' + str(SEM) + ')'
            results.loc['ICC',variable] = ICC
            results.loc['ICC_CI',variable] = ICC_CI
            results.loc['MDC',variable] = MDC
            results.loc['MDC_SEM',variable] = MDC_SEM
            
            test = xls.loc[0::2 , variable]
            meantest = np.mean(test)
            stdtest = np.std(test)
            
            hertest = xls.loc[1::2, variable]
            meanhertest = np.mean(hertest)
            stdhertest = np.std(hertest)
                
            first = str(round(meantest,3)) + ' (' + str(round(stdtest,3)) + ')'
            second = str(round(meanhertest,3)) + ' (' + str(round(stdhertest,3)) + ')'
            
            results.loc['test_mean_std',variable] = first
            results.loc['test_mean',variable] = meantest 
            results.loc['test_std',variable] = stdtest 
            
            results.loc['hertestmean_std',variable] = second
            results.loc['hertestmean',variable] = meanhertest
            results.loc['hertest_std',variable] = stdhertest 
                      
            
        if measurement == 'FM':
            saveDirectory = mainDirectory + '/Results_MakingSense/ICC single measurement'
            os.chdir(saveDirectory)
        elif measurement == 'AM':
            saveDirectory = mainDirectory + '/Results_MakingSense/ICC averaged measurement'
            os.chdir(saveDirectory)       
            
        results = results.transpose()
        save_xls = filename + '_ICC.xlsx'
        results.to_excel(save_xls)
        
        os.chdir(mainDirectory)
     

if __name__ == '__main__':
#    calculateICCMDC(measurement = 'FM')
    calculateICCMDC(measurement = 'AM')
    
    
    
