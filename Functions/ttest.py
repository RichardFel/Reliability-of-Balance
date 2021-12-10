import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.transforms
from sklearn import preprocessing

sns.set_style("darkgrid")
#sns.set_context("paper",font_scale=1.25)

mainDirectory = '/Users/richard/Library/Mobile Documents/com~apple~CloudDocs/Desktop/PhD/Algorithms PhD/Beroerte/Reliability of Balance'
directory = mainDirectory + '/Results_MakingSense/Single measurement/'

xls1 = pd.read_excel(str(directory + 'FM_Zitten.xlsx'), index_col = 0)
xls2= pd.read_excel(str(directory + 'FM_Staan.xlsx'), index_col = 0)
xls3= pd.read_excel(str(directory + 'FM_Staan voeten samen.xlsx'), index_col = 0)
xls4 = pd.read_excel(str(directory + 'FM_Staan ogen dicht.xlsx'), index_col = 0)
xls5= pd.read_excel(str(directory + 'FM_Staan op foam.xlsx'), index_col = 0)
xlslist = [xls1,xls2,xls3,xls4,xls5]


fig1, axICC = plt.subplots(1,figsize=(25,25),dpi = 110)
SMALL_SIZE = 16
MEDIUM_SIZE = 16
BIGGER_SIZE = 16

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
  


dataframe = pd.DataFrame(columns = ['Task','Subject Number', 'Result'])

metrics = ['ML Acc rms', 'Mag Acc mean', 'ML Total power']

for metric in metrics:
    dataframe = pd.DataFrame(columns = ['Task','Subject Number', 'Result'])

    for num, xls in enumerate(xlslist):
        taskNum = str(f'task{num}')
        for participant in xls['Subject number'].unique():
            if participant == 'S006P' or participant == 'S014P':
                continue
            try:
                value1 = xls.loc[(xls['Subject number'] == participant ) & 
                                  (xls['testType'] == 'Test' )][metric].iloc[0]
            except IndexError:
                continue
            dataframe = dataframe.append({'Task' : taskNum, 
                                          'Subject Number' :participant, 
                                          'Result' : value1}, ignore_index=True)
    
    subjList = dataframe['Subject Number'].value_counts() == 5
    subjListNumbers = subjList.loc[subjList == True].index
    test = dataframe.loc[dataframe['Subject Number'].isin(subjListNumbers)]
# Figure 1   
    test.loc[:,'Result']=(test['Result']-test['Result'].min())/(test['Result'].max()-test['Result'].min())
    sns.lineplot(data=test, x="Task", y="Result")

    
from matplotlib import ticker
a = ticker.MultipleLocator(1)
axICC.xaxis.set_major_locator(a)

    
axICC.set_ylabel('Mean outcome with 95% CI (normalised)')
axICC.set_xlabel('Balance condition')

    
labels = [item.get_text() for item in axICC.get_xticklabels()]

labels[0] = ''
labels[1] = 'SIT'
labels[2] = 'EO'
labels[3] = 'Ft'
labels[4] = 'EC'
labels[5] = 'FO'

axICC.set_xticklabels(labels)
axICC.set_title('Figure 1. Trendline of three sway features')
#axICC.set_ylim((0.002,0.02))



#plt.errorbar(x,y,  yerr=y_error ,fmt='o', markersize=8)


# Average value



axICC.legend(labels = ['4. ML Acc rms', '13. Mag Acc mean', '28. ML Total power'])



