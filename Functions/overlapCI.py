import os

import pandas as pd

import numpy as np

mainDirectory = '/Users/richard/Library/Mobile Documents/com~apple~CloudDocs/Desktop/PhD/Algorithms PhD/Beroerte/Reliability of Balance'

def overlap():
    resultsFM =  '/Results_MakingSense/ICC single measurement/'
    resultsAM = '/Results_MakingSense/ICC averaged measurement/'
    EOFM = pd.read_excel(str(mainDirectory +resultsFM+ '/FM_Staan_ICC.xlsx'), index_col = 0)
    EOAM = pd.read_excel(str(mainDirectory +resultsAM+ '/AM_Staan_ICC.xlsx'), index_col = 0)
    ECFM =pd.read_excel(str(mainDirectory +resultsFM+ '/FM_Staan ogen dicht_ICC.xlsx'), index_col = 0)
    ECAM =pd.read_excel(str(mainDirectory +resultsAM+ '/AM_Staan ogen dicht_ICC.xlsx'), index_col = 0)
    FTFM= pd.read_excel(str(mainDirectory +resultsFM+ '/FM_Staan voeten samen_ICC.xlsx'), index_col = 0)
    FTAM=pd.read_excel(str(mainDirectory +resultsAM+ '/AM_Staan voeten samen_ICC.xlsx'), index_col = 0)
    FOFM=pd.read_excel(str(mainDirectory +resultsFM+ '/FM_Staan op foam_ICC.xlsx'), index_col = 0)
    FOAM =pd.read_excel(str(mainDirectory +resultsAM+ '/AM_Staan op foam_ICC.xlsx'), index_col = 0)
    
    for fm, am in [(EOFM, EOAM),(ECFM, ECAM),(FTFM, FTAM),(FOFM, FOAM)]:
        counter1 = 0
        counter2 = 0
        for var1, var2 in zip(fm.iterrows(),am.iterrows()):
            if ((var1[1].ICC >= 0.75) & (var2[1].ICC >= 0.75)):
                x = np.arange(var1[1].CImin, var1[1].CImax,0.01)
                y = np.arange(var2[1].CImin, var2[1].CImax,0.01)
                
                overlap = np.arange(max(x[0], y[0]), min(x[-1], y[-1]), 0.01)
                counter1 += 1
                if len(overlap) > 0:
                    counter2 += 1
        print(f'Total reliable features: {counter1}')
        print(f'Features with overlap: {counter2}')

        