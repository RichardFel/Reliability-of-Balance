import os

import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
from matplotlib import ticker


iccValue = 0.75
target = np.ones(35) * iccValue
mainDirectory = os.getcwd()
saveTo = mainDirectory + '/Figures'


directory = mainDirectory + '/Results_MakingSense/ICC single measurement'
#fig1, axICC = plt.subplots(1,3,figsize=(25,25),dpi = 110,  gridspec_kw={'width_ratios': [(21/35), (8/35), (6/35)]})
sns.set_style("darkgrid")
sns.despine()
sns.set_context("paper",font_scale=1.25)
plt.tight_layout()

plt.subplots_adjust(left=0.05, bottom=0.2, right=None, top=0.95, wspace=0.02, hspace=0.05)
    
# Zitten
filename = 'zitten'
afkorting = 'SIT'
os.chdir(directory)
loadfile = 'FM_' + filename + '_ICC.xlsx'
xls = pd.read_excel(loadfile)
os.chdir(mainDirectory)
icc = xls.ICC 
xaxis = range(1,len(icc)+1)

mdc = np.ones(35) * 1000
for i in range(len(xls)):
    if xls.ICC[i] > iccValue:
        mdc[i] = (xls.MDC[i] / ((xls.test_std[i] + xls.hertest_std[i])/2))
        
data_plot1 = pd.DataFrame({'ICC':icc, 'Minimal ICC':target, 'xaxis':xaxis, 'MDC':mdc})
data_plot1['Type']  = 0
data_plot1.loc[0:20,'Type'] = 'Spatio-Temporal features' 
data_plot1.loc[21:28,'Type'] = 'Frequency features' 
data_plot1.loc[29:36,'Type'] = 'Complexity features' 
data_plot1['Measurement'] = 'SIT' 

# Staan
filename = 'Staan'
afkorting = 'EO'
os.chdir(directory)
loadfile = 'FM_' + filename + '_ICC.xlsx'
xls = pd.read_excel(loadfile)
os.chdir(mainDirectory)
icc = xls.ICC 
xaxis = range(1,len(icc)+1)

mdc = np.ones(35) * 1000
for i in range(len(xls)):
    if xls.ICC[i] > iccValue:
        mdc[i] = (xls.MDC[i] / ((xls.test_std[i] + xls.hertest_std[i])/2))
        
data_plot2 = pd.DataFrame({'ICC':icc, 'Minimal ICC':target, 'xaxis':xaxis, 'MDC':mdc})
data_plot2['Type']  = 0
data_plot2.loc[0:20,'Type'] = 'Spatio-Temporal features' 
data_plot2.loc[21:28,'Type'] = 'Frequency features' 
data_plot2.loc[29:36,'Type'] = 'Complexity features' 
data_plot2['Measurement'] = 'EO' 

# Ogen dicht
filename = 'Staan ogen dicht'
afkorting = 'EC'
os.chdir(directory)
loadfile = 'FM_' + filename + '_ICC.xlsx'
xls = pd.read_excel(loadfile)
os.chdir(mainDirectory)
icc = xls.ICC 
xaxis = range(1,len(icc)+1)

mdc = np.ones(35) * 1000
for i in range(len(xls)):
    if xls.ICC[i] > iccValue:
        mdc[i] = (xls.MDC[i] / ((xls.test_std[i] + xls.hertest_std[i])/2))
        
data_plot3 = pd.DataFrame({'ICC':icc, 'Minimal ICC':target, 'xaxis':xaxis, 'MDC':mdc})
data_plot3['Type']  = 0
data_plot3.loc[0:20,'Type'] = 'Spatio-Temporal features' 
data_plot3.loc[21:28,'Type'] = 'Frequency features' 
data_plot3.loc[29:36,'Type'] = 'Complexity features' 
data_plot3['Measurement'] = 'EC' 

# FT
filename = 'Staan voeten samen'
afkorting = 'FT'
os.chdir(directory)
loadfile = 'FM_' + filename + '_ICC.xlsx'
xls = pd.read_excel(loadfile)
os.chdir(mainDirectory)
icc = xls.ICC 
xaxis = range(1,len(icc)+1)

mdc = np.ones(35) * 1000
for i in range(len(xls)):
    if xls.ICC[i] > iccValue:
        mdc[i] = (xls.MDC[i] / ((xls.test_std[i] + xls.hertest_std[i])/2))
        
data_plot5 = pd.DataFrame({'ICC':icc, 'Minimal ICC':target, 'xaxis':xaxis, 'MDC':mdc})
data_plot5['Type']  = 0
data_plot5.loc[0:20,'Type'] = 'Spatio-Temporal features' 
data_plot5.loc[21:28,'Type'] = 'Frequency features' 
data_plot5.loc[29:36,'Type'] = 'Complexity features' 
data_plot5['Measurement'] = 'FT' 

# Foam
filename = 'Staan op foam'
afkorting = 'FO'
os.chdir(directory)
loadfile = 'FM_' + filename + '_ICC.xlsx'
xls = pd.read_excel(loadfile)
os.chdir(mainDirectory)
icc = xls.ICC 
xaxis = range(1,len(icc)+1)

mdc = np.ones(35) * 1000
for i in range(len(xls)):
    if xls.ICC[i] > iccValue:
        mdc[i] = (xls.MDC[i] / ((xls.test_std[i] + xls.hertest_std[i])/2))
        
data_plot4 = pd.DataFrame({'ICC':icc, 'Minimal ICC':target, 'xaxis':xaxis, 'MDC':mdc})
data_plot4['Type']  = 0
data_plot4.loc[0:20,'Type'] = 'Spatio-Temporal features' 
data_plot4.loc[21:28,'Type'] = 'Frequency features' 
data_plot4.loc[29:36,'Type'] = 'Complexity features' 
data_plot4['Measurement'] = 'FO' 

 

data_plot = pd.concat((data_plot1,data_plot2, data_plot3, data_plot5, data_plot4), ignore_index = True)


#line1 = sns.lineplot(x = 'xaxis', y = 'ICC', data = data_plot.loc[data_plot.Type == 'Spatio-Temporal features'], ax=axICC[0],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
#line2 = sns.lineplot(x = 'xaxis', y = 'ICC', data = data_plot.loc[data_plot.Type == 'Frequency features'], ax=axICC[1],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
#line3 = sns.lineplot(x = 'xaxis', y = 'ICC', data = data_plot.loc[data_plot.Type == 'Complexity features'], ax=axICC[2],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
#
#ms = line1.lines[0].get_markersize() * 1.2
#for i in range(5):
#    ms *= 0.9
#    line1.lines[i].set_linestyle("")
#    line1.lines[i].set_marker("^")
#    
#    line1.lines[i].set_markersize(ms)
#    
#    line2.lines[i].set_linestyle("")
#    line2.lines[i].set_marker("^")
#    line2.lines[i].set_markersize(ms)
#    
#    line3.lines[i].set_linestyle("")
#    line3.lines[i].set_label(afkorting)
#    line3.lines[i].set_marker("^")
#    line3.lines[i].set_markersize(ms)
#    
#sns.lineplot(x = 'xaxis', y = 'Minimal ICC', data = data_plot.loc[data_plot.Type == 'Spatio-Temporal features'], ax=axICC[0], label = 'Minimal ICC', color = 'black')
#sns.lineplot(x = 'xaxis', y = 'Minimal ICC', data = data_plot.loc[data_plot.Type == 'Frequency features'], ax=axICC[1], label = 'Minimal ICC', color = 'black')
#sns.lineplot(x = 'xaxis', y = 'Minimal ICC', data = data_plot.loc[data_plot.Type == 'Complexity features'], ax=axICC[2], label = 'Minimal ICC', color = 'black')
#    
#    
#handles, labels = axICC[2].get_legend_handles_labels()
#print(labels)
#display = (0, 1,2,3,4)
#labels = ['SIT', 'EO', 'EC', 'FT', 'FO']
#axICC[2].legend([handle for i,handle in enumerate(handles) if i in display],
#      [label for i,label in enumerate(labels) if i in display], loc = 'lower right')
#
#axICC[0].get_legend().remove()
#axICC[1].get_legend().remove()
#
#a = ticker.MultipleLocator(1)
#b = ticker.MultipleLocator(1)
#c = ticker.MultipleLocator(1)
#
#axICC[0].xaxis.set_major_locator(a)
#axICC[1].xaxis.set_major_locator(b)
#axICC[2].xaxis.set_major_locator(c)
#
#
#axICC[0].set_ylim((0,1.0))
#axICC[1].set_ylim((0,1))
#axICC[2].set_ylim((0,1))
#axICC[2].set_xlim((29,36))
#axICC[1].set_yticklabels([])
#axICC[2].set_yticklabels([])
#axICC[0].set_xticklabels([])
#axICC[1].set_xticklabels([])
#axICC[2].set_xticklabels([])
#
#axICC[0].set_xlabel('')
#axICC[0].set_ylabel('ICC')
#axICC[1].set_xlabel('')
#axICC[1].set_ylabel('')
#axICC[2].set_xlabel('')
#axICC[2].set_ylabel('')
#axICC[0].set_title('Spatio-temporal features')
#axICC[1].set_title('Frequency features')
#axICC[2].set_title('Complexity features')
# 
#
#varNames = xls.iloc[:,0]
#for number, value in enumerate(varNames):
#    num = number+1
#    varNames.iloc[number] = str(f'{num}. ' + value)
#    
#tD = varNames[0:21]
#fD = varNames[21:29]
#cO  = varNames[29:35]
#
#labels = [item.get_text() for item in axICC[0].get_xticklabels()]
#
#labels[1] = ''
#
#labels[2:23] = tD
#labels[0] = ''
#labels[23] = ''
#
#axICC[0].set_xticklabels(labels,rotation = 45, ha = 'right', rotation_mode="anchor")
#
#
## Frequency features
#labels = [item.get_text() for item in axICC[1].get_xticklabels()]
#
#labels[1:10] = fD
#labels[0] = ''
##labels[] = ''
##labels[23] = ''
#
#axICC[1].set_xticklabels(labels,rotation = 45, ha = 'right', rotation_mode="anchor")
#
#
## Complexity features
#labels = [item.get_text() for item in axICC[2].get_xticklabels()]
#
#labels[2:8] = cO
#labels[0] = ''
#labels[1] = ''
#
##labels[] = ''
##labels[23] = ''
#
#axICC[2].set_xticklabels(labels, rotation = 45, ha = 'right', rotation_mode="anchor")
#os.chdir(saveTo)
#plt.savefig('SIT.png', dpi = 600)
#
#os.chdir(mainDirectory)
##handles, labels = axICC[1,2].get_legend_handles_labels()
#display = (0,1)
#axICC[1,2].legend(['First measurement'], loc = 'upper right')
#
#axICC[1].set_title('SIT: Minimal detectable change')
#


# Lineplot 
new_dataframe = pd.DataFrame(columns = ['Measurement'])

for balance_type in data_plot['Measurement'].unique():
    tmpdf = data_plot.loc[data_plot['Measurement'] == balance_type]
    bestICC = tmpdf.iloc[[1,3,5,8,10,12,14,17,25,26,27,28,33],:]
    for i in bestICC['ICC']:
        if balance_type == 'SIT':
            translation = 'Zitten'
        if balance_type == 'EO':
            translation = 'Staan'
        if balance_type == 'EC':
            translation = 'Ogen dicht'
        if balance_type == 'FT':
            translation = 'Voeten tegen elkaar'
        if balance_type == 'FO':
            translation = 'Foam'
        new_dataframe = new_dataframe.append({'Measurement':translation,
                                              'ICC': i}, ignore_index = True)

    
fig1, axICC = plt.subplots(figsize=(10,15),dpi = 110)
line1 = sns.pointplot(data = new_dataframe, x = 'Measurement', y = 'ICC', linestyles = '', ci = 'sd', capsize=.1, hue = 'Measurement', ax = axICC)
ms = line1.lines[0].get_markersize() * 3
axICC.set_ylim((0,1.0))

for num, i in enumerate(data_plot['Measurement'].unique()): 
    line1.lines[num].set_markersize(ms)


line2 = sns.pointplot(x = ['Zitten', 'Staan', 'Ogen dicht', 'Voeten tegen elkaar', 'Foam'], y = [0.75,0.75,0.75,0.75,0.75], ax = axICC, markers = '', color = 'black')

handles, labels = axICC.get_legend_handles_labels()
from matplotlib.lines import Line2D
line = Line2D([0], [0], label='cut-off line', color='black')
handles.extend([line])
axICC.legend(handles=handles,  loc = 'lower left').legendHandles[0]._sizes = [15]  
axICC.set_xlabel('')
fig1.show()




# Lineplot MDC & BBS
fase1 = pd.read_excel('Dataset fase 1.xlsx', index_col = 0)
zitten = pd.read_excel('FM_Zitten.xlsx', index_col = 0)
staan = pd.read_excel('FM_Staan.xlsx', index_col = 0)
ogendicht=pd.read_excel('FM_Staan ogen dicht.xlsx', index_col = 0)
voetensamen=pd.read_excel('FM_Staan voeten samen.xlsx', index_col = 0)
foam =pd.read_excel('FM_Staan op foam.xlsx', index_col = 0)

for i in [zitten, staan, ogendicht, voetensamen, foam]:
    a = i.groupby('Subject number').size()
    a = a.loc[a == 2]
    i = i.loc[i['Subject number'].isin(a.index)]
    descriptives = fase1.loc[fase1.index.isin(i['Subject number'])]
    print(descriptives['BBS_totaal'].std())
    print(6 / descriptives['BBS_totaal'].std())


new_dataframe = pd.DataFrame(columns = ['Measurement'])

for balance_type in data_plot['Measurement'].unique():
    tmpdf = data_plot.loc[data_plot['Measurement'] == balance_type]
    bestICC = tmpdf.iloc[[1,3,5,8,10,12,14,17,25,26,27,28,33],:]
    for i in bestICC['MDC']:
        if balance_type == 'SIT':
            translation = 'Zitten'
        if balance_type == 'EO':
            translation = 'Staan'
        if balance_type == 'EC':
            translation = 'Ogen dicht'
        if balance_type == 'FT':
            translation = 'Voeten tegen elkaar'
        if balance_type == 'FO':
            translation = 'Foam'
        new_dataframe = new_dataframe.append({'Measurement':translation,
                                              'MDC/STD': i}, ignore_index = True)

    
fig1, axICC = plt.subplots(figsize=(10,15),dpi = 110)
line1 = sns.pointplot(data = new_dataframe, x = 'Measurement', 
                      y = 'MDC/STD', linestyles = '', 
                      ci = 'sd', capsize=.1, 
                      hue = 'Measurement', 
                      ax = axICC, 
                      markersize = 10)
ms = line1.lines[0].get_markersize() * 10
axICC.set_ylim((0,1.5))

for num, i in enumerate(data_plot['Measurement'].unique()): 
    line1.lines[num].set_markersize(ms)


line2 = sns.pointplot(x = ['Zitten', 'Staan', 'Ogen dicht', 'Voeten tegen elkaar', 'Foam'], 
                      y = [0.36,0.55,0.6,0.72,0.72], 
                      ax = axICC, 
                      markers = '*', 
                      linestyles = '',
                      color = 'black')

ms = line2.lines[0].get_markersize() * 10
line1.lines[1].set_markersize(ms)

handles, labels = axICC.get_legend_handles_labels()
from matplotlib.lines import Line2D
line = Line2D([0], [0], label='BBS', color='black', marker = '*', linestyle = '')
handles.extend([line])
axICC.legend(handles=handles,  loc = 'lower left').legendHandles[0]._sizes = [15]  
axICC.set_xlabel('')

fig1.show()


