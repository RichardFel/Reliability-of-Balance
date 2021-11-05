import os

import pandas as pd


mainDirectory = os.getcwd()

icc_min = 0.75


def meanStdtoLatex(measurement):
    if measurement == 'FM':
            directory = mainDirectory + '/Results_MakingSense/ICC single measurement'
            os.chdir(directory)

    elif measurement == 'AM':
            directory = mainDirectory + '/Results_MakingSense/ICC averaged measurement'
            os.chdir(directory)       
   
    if measurement == 'FM':
        xls1 = pd.read_excel('FM_Zitten_ICC.xlsx', index_col = 0)
        
    xls2= pd.read_excel(f'{measurement}_Staan_ICC.xlsx', index_col = 0)
    xls3= pd.read_excel(f'{measurement}_Staan voeten samen_ICC.xlsx', index_col = 0)
    xls4 = pd.read_excel(f'{measurement}_Staan ogen dicht_ICC.xlsx', index_col = 0)
    xls5= pd.read_excel(f'{measurement}_Staan op foam_ICC.xlsx', index_col = 0)
    
    print('\n' + f'Mean and STD of {measurement}' + '\n')
    for k in range(len(xls2)):  # MEAN AND STD OF FM
        
        all_true = True
        a_true = True 
        c_true = True
        e_true = True
        g_true = True
        i_true = True
        idx = xls2.index[k]
        idx = str(k + 1) +  '. ' + idx
        if measurement == 'FM':
            a = xls1['test_mean_std'].iloc[k]
            b = xls1['hertestmean_std'].iloc[k]
            
        c = xls2['test_mean_std'].iloc[k]
        d = xls2['hertestmean_std'].iloc[k]
        e = xls3['test_mean_std'].iloc[k]
        f = xls3['hertestmean_std'].iloc[k]
        g = xls4['test_mean_std'].iloc[k]
        h = xls4['hertestmean_std'].iloc[k]
        i = xls5['test_mean_std'].iloc[k]
        j = xls5['hertestmean_std'].iloc[k]    
    
        if measurement == 'FM':
            if xls1.ICC.iloc[k] >= icc_min:
                a = str(' \ textbf{' + a + '}')
                b  = str(' \ textbf{' + b + '}')
            else:
                all_true = False
                a_true = False
                
        if xls2.ICC.iloc[k] >= icc_min:
            c = str(' \ textbf{' + c + '}')
            d  = str(' \ textbf{' + d + '}')
        else:
            all_true = False
            c_true = False
        if xls3.ICC.iloc[k] >= icc_min:
            e = str(' \ textbf{' + e + '}')
            f  = str(' \ textbf{' + f + '}')
        else:
            all_true = False
            e_true = False
        if xls4.ICC.iloc[k] >= icc_min:
            g = str(' \ textbf{' + g + '}')
            h  = str(' \ textbf{' + h + '}')
        else:
            all_true = False
            g_true = False
        if xls5.ICC.iloc[k] >= icc_min:
            i = str(' \ textbf{' + i + '}')
            j = str(' \ textbf{' + j + '}')
        else:
            all_true = False
            i_true = False
    
    
        if measurement == 'FM':
            if all_true == True:
                idx = str(idx) + ' **'
            
            elif a_true == True:
                idx = str(idx) + ' *'
            elif c_true == True:
                idx = str(idx) + ' *'
            elif e_true == True:
                idx = str(idx) + ' *'
            elif g_true == True:
                idx = str(idx) + ' *'    
            elif i_true == True:
                idx = str(idx) + ' *'
            else:
                idx = str(idx)
                
        else:
            if all_true == True:
                idx = str(idx) + ' **'
            elif c_true == True:
                idx = str(idx) + ' *'
            elif e_true == True:
                idx = str(idx) + ' *'
            elif g_true == True:
                idx = str(idx) + ' *'    
            elif i_true == True:
                idx = str(idx) + ' *'
            else:
                idx = str(idx)
            
        if k == 21:
            print('\midrule')
            print('\n')
        elif k == 29:
            print('\midrule')
            print('\n')
            
        if measurement == 'FM':
            print(str('&' + idx + '&' + a + '&' + b + '&' + '&' + c + '&' + d +'&' +
                      '&' + e +'&' + f +'&' +'&' + g +'&' + h +'&' + '&' + i +
                      '&' + j + ' \ \ '))
        else:
            print(str('&' + idx + '&' + c + '&' + d +'&' +
                          '&' + e +'&' + f +'&' +'&' + g +'&' + h +'&' + '&' + i +
                          '&' + j + ' \ \ '))
    
def iccmdctoLatex(measurement):
    if measurement == 'FM':
            directory = mainDirectory + '/Results_MakingSense/ICC single measurement'
            os.chdir(directory)

    elif measurement == 'AM':
            directory = mainDirectory + '/Results_MakingSense/ICC averaged measurement'
            os.chdir(directory)       
   
    if measurement == 'FM':
        xls1 = pd.read_excel('FM_Zitten_ICC.xlsx', index_col = 0)
        
    xls2= pd.read_excel(f'{measurement}_Staan_ICC.xlsx', index_col = 0)
    xls3= pd.read_excel(f'{measurement}_Staan voeten samen_ICC.xlsx', index_col = 0)
    xls4 = pd.read_excel(f'{measurement}_Staan ogen dicht_ICC.xlsx', index_col = 0)
    xls5= pd.read_excel(f'{measurement}_Staan op foam_ICC.xlsx', index_col = 0)



    print('\n' + f'ICC and MDC as percentage of mean of {measurement}' + '\n')
    for k in range(len(xls2)): # ICC and MDC as percentage of mean
        
        all_true = True
        
        a_true = True
        c_true = True
        e_true = True
        g_true = True
        i_true = True
        
        idx = xls2.index[k]
        idx = str(k + 1) +  '. ' + idx
        
        if measurement == 'FM':
            a = xls1['ICC_CI'].iloc[k]
            if xls1.ICC.iloc[k] >= icc_min:
                a = str(' \ textbf{' + a + '}')
            else: 
                all_true = False
                a_true = False        
            
            b = ''
            if xls1.ICC.iloc[k] >= icc_min:
                b = str(((xls1.MDC.iloc[k] / ((xls1.test_std.iloc[k] + xls1.hertest_std.iloc[k])/2)).round(1)))
                    
        c = xls2['ICC_CI'].iloc[k]
        if xls2.ICC.iloc[k] >= icc_min:
            c = str(' \ textbf{' + c + '}')
        else:
            all_true = False
            c_true = False   
            
        d = ''
        if xls2.ICC.iloc[k] >= icc_min:
            d = str(((xls2.MDC.iloc[k] / ((xls2.test_std.iloc[k] + xls2.hertest_std.iloc[k])/2)).round(1)))
    
        e = xls3['ICC_CI'].iloc[k]
        if xls3.ICC.iloc[k] >= icc_min:
            e = str(' \ textbf{' + e + '}')
        else:
            all_true = False
            e_true = False  
            
        f = ''
        if xls3.ICC.iloc[k] >= icc_min:
            f = str(((xls3.MDC.iloc[k] / ((xls3.test_std.iloc[k] + xls3.hertest_std.iloc[k])/2)).round(1)))
    
        g = xls4['ICC_CI'].iloc[k]
        if xls4.ICC.iloc[k] >= icc_min:
            g = str(' \ textbf{' + g + '}')
        else:
            all_true = False
            g_true = False  
            
        h = ''
        if xls4.ICC.iloc[k] >= icc_min:
            h = str(((xls4.MDC.iloc[k] / ((xls4.test_std.iloc[k] + xls4.hertest_std.iloc[k])/2)).round(1)))
               
        i = xls5['ICC_CI'].iloc[k]
        if xls5.ICC.iloc[k] >= icc_min:
            i = str(' \ textbf{' + i + '}')
        else:
            all_true = False
            i_true = False  
          
        j = ''
        if xls5.ICC.iloc[k] >= icc_min:
            j = str(((xls5.MDC.iloc[k] / ((xls5.test_std.iloc[k] + xls5.hertest_std.iloc[k])/2)).round(1)))
    
        if measurement == 'FM':   
            if all_true == True:
                idx = str(idx) + ' **'
            elif a_true == True:
                idx = str(idx) + ' *'
            elif a_true == True:
                idx = str(idx) + ' *'
            elif c_true == True:
                idx = str(idx) + ' *'
            elif e_true == True:
                idx = str(idx) + ' *'
            elif g_true == True:
                idx = str(idx) + ' *'    
            elif i_true == True:
                idx = str(idx) + ' *'
            else:
                idx = str(idx)
        else:
            if all_true == True:
                idx = str(idx) + ' **'
            elif c_true == True:
                idx = str(idx) + ' *'
            elif e_true == True:
                idx = str(idx) + ' *'
            elif g_true == True:
                idx = str(idx) + ' *'    
            elif i_true == True:
                idx = str(idx) + ' *'
            else:
                idx = str(idx)           
            
        if k == 21:
            print('\midrule')
            print('\n')
        elif k == 29:
            print('\midrule')
            print('\n')
            
        if measurement == 'FM': 
            print(str('&'  + idx  + '&' + a + '&' + b + '&' + '&' + c + '&' + d +'&' +
                      '&' + e +'&' + f +'&' +'&' + g +'&' + h +'&' + '&' + i +
                      '&' + j + ' \ \ '))
        else:
            print(str('&'  + idx  + '&' + c + '&' + d +'&' +
                      '&' + e +'&' + f +'&' +'&' + g +'&' + h +'&' + '&' + i +
                      '&' + j + ' \ \ '))        
        
def mdcRawToLatex():
    directory = mainDirectory + '/Results_MakingSense/ICC single measurement'
    os.chdir(directory)
    xls1 = pd.read_excel('FM_Zitten_ICC.xlsx', index_col = 0)
    xls2= pd.read_excel('FM_Staan_ICC.xlsx', index_col = 0)
    xls3= pd.read_excel('FM_Staan voeten samen_ICC.xlsx', index_col = 0)
    xls4 = pd.read_excel('FM_Staan ogen dicht_ICC.xlsx', index_col = 0)
    xls5= pd.read_excel('FM_Staan op foam_ICC.xlsx', index_col = 0)

    directory = mainDirectory + '/Results_MakingSense/ICC averaged measurement'
    os.chdir(directory)       
    xls6= pd.read_excel('AM_Staan_ICC.xlsx', index_col = 0)
    xls7= pd.read_excel('AM_staan voeten samen_ICC.xlsx', index_col = 0)
    xls8 = pd.read_excel('AM_staan ogen dicht_ICC.xlsx', index_col = 0)
    xls9= pd.read_excel('AM_staan op foam_ICC.xlsx', index_col = 0)
    
    print('\n' + 'MDC & SEM' + '\n')
    
    for k in range(len(xls1)): # MDC and SEM
        
        all_true = True
        a_true = True
        c_true = True
        e_true = True
        g_true = True
        i_true = True
        
        idx = xls1.index[k]
        idx = str(k + 1) +  '. ' + idx
    
        a = ''
        if xls1.ICC.iloc[k] >= icc_min:
            a = str(xls1['MDC_SEM'].iloc[k])
        else: 
            all_true = False
            a_true = False        
            
        b = ''
                
        c = ''
        if xls2.ICC.iloc[k] >= icc_min:
            c = str(xls2['MDC_SEM'].iloc[k])
        else:
            all_true = False
            c_true = False   
            
        d = ''
        if xls6.ICC.iloc[k] >= icc_min:
            d = str(xls6['MDC_SEM'].iloc[k])
        else:
            all_true = False
            c_true = False  
            
        e = ''
        if xls3.ICC.iloc[k] >= icc_min:
            e = str(xls3['MDC_SEM'].iloc[k])
        else:
            all_true = False
            e_true = False  
            
        f = ''
        if xls7.ICC.iloc[k] >= icc_min:
            f = str(xls7['MDC_SEM'].iloc[k])
        else:
            all_true = False
            e_true = False  
            
        g = ''
        if xls4.ICC.iloc[k] >= icc_min:
            g = str(xls4['MDC_SEM'].iloc[k])
        else:
            all_true = False
            g_true = False  
            
        h = ''
        if xls8.ICC.iloc[k] >= icc_min:
            h = str(xls8['MDC_SEM'].iloc[k])
        else:
            all_true = False
            g_true = False  
               
        i = ''
        if xls5.ICC.iloc[k] >= icc_min:
            i = str(xls5['MDC_SEM'].iloc[k])
        else:
            all_true = False
            i_true = False  
          
        j = ''
        if xls9.ICC.iloc[k] >= icc_min:
            j= str(xls9['MDC_SEM'].iloc[k])
        else:
            all_true = False
            i_true = False 
            
        if all_true == True:
            idx = str(idx) + ' **'
        elif a_true == True:
            idx = str(idx) + ' *'
        elif a_true == True:
            idx = str(idx) + ' *'
        elif c_true == True:
            idx = str(idx) + ' *'
        elif e_true == True:
            idx = str(idx) + ' *'
        elif g_true == True:
            idx = str(idx) + ' *'    
        elif i_true == True:
            idx = str(idx) + ' *'
        else:
            idx = str(idx)
       
            
        if k == 21:
            print('\midrule')
            print('\n')
        elif k == 29:
            print('\midrule')
            print('\n')
        print(str('&'  + idx  + '&' + a + '&' + b + '&' + '&' + c + '&' + d +'&' +
                  '&' + e +'&' + f +'&' +'&' + g +'&' + h +'&' + '&' + i +
                  '&' + j + ' \ \ '))
          
if __name__ == "__main__":
    meanStdtoLatex('FM')
    iccmdctoLatex('FM')
    
    meanStdtoLatex('AM')
    iccmdctoLatex('AM')
    
    mdcRawToLatex()
    
    

        
    