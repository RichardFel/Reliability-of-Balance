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

def plotSIT():
    directory = mainDirectory + '/Results/ICC single measurement'
    os.chdir(directory)
    loadfile = 'FM_Zitten_ICC.xlsx'
    xls = pd.read_excel(loadfile)
    os.chdir(mainDirectory)
    icc = xls.ICC 
    xaxis = range(1,len(icc)+1)
    
    mdc = np.ones(35) * 1000
    for i in range(len(xls)):
        if xls.ICC[i] > iccValue:
            mdc[i] = (xls.MDC[i] / ((xls.test_std[i] + xls.hertest_std[i])/2))

    data_plot = pd.DataFrame({'ICC':icc, 'Minimal ICC':target, 'xaxis':xaxis, 'MDC':mdc})
    data_plot['Type']  = 0
    data_plot.loc[0:20,'Type'] = 'Spatio-Temporal features' 
    data_plot.loc[21:28,'Type'] = 'Frequency features' 
    data_plot.loc[29:36,'Type'] = 'Complexity features' 
    data_plot['Measurement'] = 'FM' 
    
    sns.set_style("darkgrid")
    sns.despine()
    sns.set_context("paper",font_scale=1.25)
    
    
    fig1, axICC = plt.subplots(2,3,figsize=(25,25),dpi = 110, gridspec_kw={'width_ratios': [(21/35), (8/35), (6/35)]})
    plt.tight_layout()
    
    plt.subplots_adjust(left=0.05, bottom=0.15, right=None, top=0.95, wspace=0.02, hspace=0.05)
    
    
    line1 = sns.lineplot(x = 'xaxis', y = 'ICC', data = data_plot.loc[data_plot.Type == 'Spatio-Temporal features'], ax=axICC[0,0],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
    line2 = sns.lineplot(x = 'xaxis', y = 'ICC', data = data_plot.loc[data_plot.Type == 'Frequency features'], ax=axICC[0,1],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
    line3 = sns.lineplot(x = 'xaxis', y = 'ICC', data = data_plot.loc[data_plot.Type == 'Complexity features'], ax=axICC[0,2],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
    
    line4 = sns.lineplot(x = 'xaxis', y = 'Minimal ICC', data = data_plot.loc[data_plot.Type == 'Spatio-Temporal features'], ax=axICC[0,0], label = 'Minimal ICC', color = 'black')
    line5 = sns.lineplot(x = 'xaxis', y = 'Minimal ICC', data = data_plot.loc[data_plot.Type == 'Frequency features'], ax=axICC[0,1], label = 'Minimal ICC', color = 'black')
    line6 = sns.lineplot(x = 'xaxis', y = 'Minimal ICC', data = data_plot.loc[data_plot.Type == 'Complexity features'], ax=axICC[0,2], label = 'Minimal ICC', color = 'black')
    #    
    line1.lines[0].set_linestyle("")
    line1.lines[0].set_label('FM: Spatio-Temporal features')
    line1.lines[0].set_marker("^")
    ms = line1.lines[0].get_markersize()
    line1.lines[0].set_markersize(ms * 1.5)
    
    
    line2.lines[0].set_linestyle("")
    line2.lines[0].set_label('FM: Frequency features')
    line2.lines[0].set_marker("^")
    line2.lines[0].set_markersize(ms * 1.5)
    
    line3.lines[0].set_linestyle("")
    line3.lines[0].set_label('First Measurement')
    line3.lines[0].set_marker("^")
    line3.lines[0].set_markersize(ms * 1.5)
    
    
    handles, labels = axICC[0,2].get_legend_handles_labels()
    display = (0,5)
    axICC[0,2].legend([handle for i,handle in enumerate(handles) if i in display],
          [label for i,label in enumerate(labels) if i in display], loc = 'lower right')
    
    axICC[0,0].get_legend().remove()
    axICC[0,1].get_legend().remove()
    
    from matplotlib import ticker
    a = ticker.MultipleLocator(1)
    b = ticker.MultipleLocator(1)
    c = ticker.MultipleLocator(1)
    
    axICC[0,0].xaxis.set_major_locator(a)
    axICC[0,1].xaxis.set_major_locator(b)
    axICC[0,2].xaxis.set_major_locator(c)
    
    
    axICC[0,0].set_ylim((0.48,1.0))
    axICC[0,1].set_ylim((0.48,1))
    axICC[0,2].set_ylim((0.48,1))
    axICC[0,2].set_xlim((29,36))
    axICC[0,1].set_yticklabels([])
    axICC[0,2].set_yticklabels([])
    axICC[0,0].set_xticklabels([])
    axICC[0,1].set_xticklabels([])
    axICC[0,2].set_xticklabels([])
    
    axICC[0,0].set_xlabel('')
    axICC[0,0].set_ylabel('ICC')
    axICC[0,1].set_xlabel('')
    axICC[0,1].set_ylabel('')
    axICC[0,2].set_xlabel('')
    axICC[0,2].set_ylabel('')
    axICC[0,0].set_title('Spatio-temporal features')
    axICC[0,1].set_title('Frequency features')
    axICC[0,2].set_title('Complexity features')
    
    
    #
    line7 = sns.lineplot(x = 'xaxis', y = 'MDC', data = data_plot.loc[data_plot.Type == 'Spatio-Temporal features'], ax=axICC[1,0],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, linewidth = 0, palette = 'deep')
    line8 = sns.lineplot(x = 'xaxis', y = 'MDC', data = data_plot.loc[data_plot.Type == 'Frequency features'], ax=axICC[1,1],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
    line9 = sns.lineplot(x = 'xaxis', y = 'MDC', data = data_plot.loc[data_plot.Type == 'Complexity features'], ax=axICC[1,2],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
    
    line7.lines[0].set_linestyle("")
    line7.lines[0].set_label('FM: Spatio-Temporal features')
    line7.lines[0].set_marker("^")
    line7.lines[0].set_markersize(ms * 1.5)
    
    line8.lines[0].set_linestyle("")
    line8.lines[0].set_label('FM: Frequency features')
    line8.lines[0].set_marker("^")
    line8.lines[0].set_markersize(ms * 1.5)
    
    line9.lines[0].set_linestyle("")
    line9.lines[0].set_label('Single Measurement')
    line9.lines[0].set_marker("^")
    line9.lines[0].set_markersize(ms * 1.5)
    
    axICC[1,0].set_ylim((0,2))
    axICC[1,1].set_ylim((0,2))
    axICC[1,2].set_ylim((0,2))
    axICC[1,2].set_xlim((29,36))
    
    #axICC[1,0].yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y/100))) 
    
    
    #axICC[1].set_xlabel('Balance Features')
    
    
    axICC[1,0].get_legend().remove()
    axICC[1,1].get_legend().remove()
    axICC[1,2].get_legend().remove()
    
    
    a = ticker.MultipleLocator(1)
    b = ticker.MultipleLocator(1)
    c = ticker.MultipleLocator(1)
    
    
    axICC[1,0].xaxis.set_major_locator(a)
    axICC[1,1].xaxis.set_major_locator(b)
    axICC[1,2].xaxis.set_major_locator(c)
    
    axICC[1,1].set_yticklabels([])
    axICC[1,2].set_yticklabels([])
    axICC[1,0].set_xlabel('')
    axICC[1,0].set_ylabel('MDC expressed as STD')
    axICC[1,1].set_xlabel('')
    axICC[1,1].set_ylabel('')
    axICC[1,2].set_xlabel('')
    axICC[1,2].set_ylabel('')
    axICC[1,0].set_title('')
    axICC[1,1].set_title('')
    axICC[1,2].set_title('')
    
    varNames = xls.iloc[:,0]
    for number, value in enumerate(varNames):
        num = number+1
        varNames.iloc[number] = str(f'{num}. ' + value)
        
    tD = varNames[0:21]
    fD = varNames[21:29]
    cO  = varNames[29:35]
    
    
    #dx = 10/72.; dy = 0/72. 
    #offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig1.dpi_scale_trans)
    #
    ## apply offset transform to all x ticklabels.
    #for label in axICC[1,0].xaxis.get_majorticklabels():
    #    label.set_transform(label.get_transform() + offset)
    #for label in axICC[1,1].xaxis.get_majorticklabels():
    #    label.set_transform(label.get_transform() + offset)
    #for label in axICC[1,2].xaxis.get_majorticklabels():
    #    label.set_transform(label.get_transform() + offset)
    #            
        
    # Spatio-Temporal features
    labels = [item.get_text() for item in axICC[1,0].get_xticklabels()]
    
    labels[1] = ''
    
    labels[2:23] = tD
    labels[0] = ''
    labels[23] = ''
    
    axICC[1,0].set_xticklabels(labels,rotation = 45, ha = 'right', rotation_mode="anchor")
    
    
    # Frequency features
    labels = [item.get_text() for item in axICC[1,1].get_xticklabels()]
    
    labels[1:10] = fD
    labels[0] = ''
    #labels[] = ''
    #labels[23] = ''
    
    axICC[1,1].set_xticklabels(labels,rotation = 45, ha = 'right', rotation_mode="anchor")
    
    
    # Complexity features
    labels = [item.get_text() for item in axICC[1,2].get_xticklabels()]
    
    labels[2:8] = cO
    labels[0] = ''
    labels[1] = ''
    
    #labels[] = ''
    #labels[23] = ''
    
    axICC[1,2].set_xticklabels(labels, rotation = 45, ha = 'right', rotation_mode="anchor")
    
    
    os.chdir(saveTo)
    plt.savefig('SIT.png', dpi = 600)
    
    os.chdir(mainDirectory)
    #handles, labels = axICC[1,2].get_legend_handles_labels()
    #display = (0,1)
    #axICC[1,2].legend(['First measurement'], loc = 'upper right')
    
    #axICC[1].set_title('SIT: Minimal detectable change')

def plotStanding():
    ######### Staan ######### 
    for i in range(4):
        if i == 0:
            filename = 'Staan'
            afkorting = 'EO'
        if i == 1:
            filename = 'Staan ogen dicht'
            afkorting = 'EC'
        if i == 2:
            filename = 'Staan op foam'
            afkorting = 'FO'
            
        if i == 3:
            filename = 'Staan voeten samen'
            afkorting = 'FT'
    
        directory = mainDirectory + '/Results/ICC single measurement'
        os.chdir(directory)
        
        loadfile = 'FM_' + filename + '_ICC.xlsx'
        xlsFM = pd.read_excel(loadfile)
    
        os.chdir(mainDirectory)
        
        icc = xlsFM.ICC 
        xaxis = range(1,len(icc)+1)
        
        mdc = np.ones(35) * 1000
        for i in range(len(xlsFM)):
            if xlsFM.ICC[i] > iccValue:
                if (xlsFM.MDC[i] / ((xlsFM.test_std[i] + xlsFM.hertest_std[i])/2) * 100) < 300:
                    mdc[i] = (xlsFM.MDC[i] / ((xlsFM.test_std[i] + xlsFM.hertest_std[i])/2))
        
        
        data_plot1 = pd.DataFrame({'ICC':icc,'Minimal ICC':target, 'xaxis':xaxis, 'MDC':mdc})
        #data_plot['Type']  = 0
        data_plot1.loc[0:20,'Type'] = 'Spatio-Temporal features' 
        data_plot1.loc[21:28,'Type'] = 'Frequency features' 
        data_plot1.loc[29:36,'Type'] = 'Complexity features' 
        data_plot1.loc[29:36,'Type'] = 'Complexity features' 
        data_plot1['Measurement'] = 'FM' 
        
        directory = mainDirectory + '/Results/ICC Averaged measurement'
        os.chdir(directory)
        
        loadfile = 'AM_' + filename + '_ICC.xlsx'
        xlsAM = pd.read_excel(loadfile)
        
        os.chdir(mainDirectory)
        
        icc = xlsAM.ICC 
        xaxis = range(1,len(icc)+1)
        
        mdc = np.ones(35) * 1000
        for i in range(len(xlsAM)):
            if xlsAM.ICC[i] > iccValue:
                if (xlsAM.MDC[i] / ((xlsAM.test_std[i] + xlsAM.hertest_std[i])/2) * 100) < 300:
                    mdc[i] = (xlsAM.MDC[i] / ((xlsAM.test_std[i] + xlsAM.hertest_std[i])/2))
            
        
        data_plot2 = pd.DataFrame({'ICC':icc,'Minimal ICC':target, 'xaxis':xaxis, 'MDC':mdc})
        #data_plot['Type']  = 0
        data_plot2.loc[0:20,'Type'] = 'Spatio-Temporal features' 
        data_plot2.loc[21:28,'Type'] = 'Frequency features' 
        data_plot2.loc[29:36,'Type'] = 'Complexity features' 
        data_plot2.loc[29:36,'Type'] = 'Complexity features' 
        data_plot2['Measurement'] = 'AM' 
        
        data_plot = pd.concat((data_plot1,data_plot2), ignore_index = True)
        
        
        fig1, axICC = plt.subplots(2,3,figsize=(25,25),dpi = 110, gridspec_kw={'width_ratios': [(21/35), (8/35), (6/35)]})
        plt.tight_layout()
        
        plt.subplots_adjust(left=0.05, bottom=0.15, right=None, top=0.95, wspace=0.02, hspace=0.05)
        
        line1 = sns.lineplot(x = 'xaxis', y = 'ICC', data = data_plot.loc[data_plot.Type == 'Spatio-Temporal features'], ax=axICC[0,0],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
        line2 = sns.lineplot(x = 'xaxis', y = 'ICC', data = data_plot.loc[data_plot.Type == 'Frequency features'], ax=axICC[0,1],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
        line3 = sns.lineplot(x = 'xaxis', y = 'ICC', data = data_plot.loc[data_plot.Type == 'Complexity features'], ax=axICC[0,2],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
        
        line4 = sns.lineplot(x = 'xaxis', y = 'Minimal ICC', data = data_plot.loc[data_plot.Type == 'Spatio-Temporal features'], ax=axICC[0,0], label = 'Minimal ICC', color = 'black')
        line5 = sns.lineplot(x = 'xaxis', y = 'Minimal ICC', data = data_plot.loc[data_plot.Type == 'Frequency features'], ax=axICC[0,1], label = 'Minimal ICC', color = 'black')
        line6 = sns.lineplot(x = 'xaxis', y = 'Minimal ICC', data = data_plot.loc[data_plot.Type == 'Complexity features'], ax=axICC[0,2], label = 'Minimal ICC', color = 'black')
        
        
        line1.lines[0].set_linestyle("")
        line1.lines[0].set_label('FM: Spatio-Temporal features')
        line1.lines[0].set_marker("^")
        ms = line1.lines[0].get_markersize()
        line1.lines[0].set_markersize(ms * 1.5)
        
        line1.lines[1].set_linestyle("")
        line1.lines[1].set_label('AM: Spatio-Temporal features')
        line1.lines[1].set_marker("^")
        
        line2.lines[0].set_linestyle("")
        line2.lines[0].set_label('FM: Frequency features')
        line2.lines[0].set_marker("^")
        line2.lines[0].set_markersize(ms * 1.5)
        
        line2.lines[1].set_linestyle("")
        line2.lines[1].set_label('AM: Frequency features')
        line2.lines[1].set_marker("^")
        
        line3.lines[0].set_linestyle("")
        line3.lines[0].set_label('Single Measurement')
        line3.lines[0].set_marker("^")
        line3.lines[0].set_markersize(ms * 1.5)
        
        line3.lines[1].set_linestyle("")
        line3.lines[1].set_label('Averaged Measurements')
        line3.lines[1].set_marker("^")
          
        handles, labels = axICC[0,2].get_legend_handles_labels()
        display = (0,1,7)
        axICC[0,2].legend([handle for i,handle in enumerate(handles) if i in display],
              [label for i,label in enumerate(labels) if i in display], loc = 'lower right')
        
        axICC[0,0].get_legend().remove()
        axICC[0,1].get_legend().remove()
        
        a = ticker.MultipleLocator(1)
        b = ticker.MultipleLocator(1)
        c = ticker.MultipleLocator(1)
        
        axICC[0,0].xaxis.set_major_locator(a)
        axICC[0,1].xaxis.set_major_locator(b)
        axICC[0,2].xaxis.set_major_locator(c)
        
        
        axICC[0,0].set_ylim((0.48,1.0))
        axICC[0,1].set_ylim((0.48,1))
        axICC[0,2].set_ylim((0.48,1))
        axICC[0,2].set_xlim((29,36))
        axICC[0,1].set_yticklabels([])
        axICC[0,2].set_yticklabels([])
        axICC[0,0].set_xticklabels([])
        axICC[0,1].set_xticklabels([])
        axICC[0,2].set_xticklabels([])
        
        axICC[0,0].set_xlabel('')
        axICC[0,0].set_ylabel('ICC')
        axICC[0,1].set_xlabel('')
        axICC[0,1].set_ylabel('')
        axICC[0,2].set_xlabel('')
        axICC[0,2].set_ylabel('')
        axICC[0,0].set_title('Spatio-temporal features')
        axICC[0,1].set_title('Frequency features')
        axICC[0,2].set_title('Complexity features')

        
        line7 = sns.lineplot(x = 'xaxis', y = 'MDC', data = data_plot.loc[data_plot.Type == 'Spatio-Temporal features'], ax=axICC[1,0],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, linewidth = 0, palette = 'deep')
        line8 = sns.lineplot(x = 'xaxis', y = 'MDC', data = data_plot.loc[data_plot.Type == 'Frequency features'], ax=axICC[1,1],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
        line9 = sns.lineplot(x = 'xaxis', y = 'MDC', data = data_plot.loc[data_plot.Type == 'Complexity features'], ax=axICC[1,2],marker = 'o', hue = 'Measurement', style = 'Type',markersize = 9, palette = 'deep')
        
        line7.lines[0].set_linestyle("")
        line7.lines[0].set_label('FM: Spatio-Temporal features')
        line7.lines[0].set_marker("^")
        line7.lines[0].set_markersize(ms * 1.5)
        
        line8.lines[0].set_linestyle("")
        line8.lines[0].set_label('FM: Frequency features')
        line8.lines[0].set_marker("^")
        line8.lines[0].set_markersize(ms * 1.5)
        
        line9.lines[0].set_linestyle("")
        line9.lines[0].set_label('First Measurement')
        line9.lines[0].set_marker("^")
        line9.lines[0].set_markersize(ms * 1.5)
        
        line7.lines[1].set_linestyle("")
        line7.lines[1].set_label('AM: Spatio-Temporal features')
        line7.lines[1].set_marker("^")
        
        line8.lines[1].set_linestyle("")
        line8.lines[1].set_label('AM: Frequency features')
        line8.lines[1].set_marker("^")
        
        line9.lines[1].set_linestyle("")
        line9.lines[1].set_label('Average Measurement')
        line9.lines[1].set_marker("^")
        
        axICC[1,0].set_ylim((0,2))
        axICC[1,1].set_ylim((0,2))
        axICC[1,2].set_ylim((0,2))
        axICC[1,2].set_xlim((29,36))
        #    axICC[1,0].yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y/100))) 
        
        
        #axICC[1].set_xlabel('Balance Features')
        
        
        axICC[1,0].get_legend().remove()
        axICC[1,1].get_legend().remove()
        axICC[1,2].get_legend().remove()
        
        a = ticker.MultipleLocator(1)
        b = ticker.MultipleLocator(1)
        c = ticker.MultipleLocator(1)
        
        axICC[1,0].xaxis.set_major_locator(a)
        axICC[1,1].xaxis.set_major_locator(b)
        axICC[1,2].xaxis.set_major_locator(c)
        
        axICC[1,1].set_yticklabels([])
        axICC[1,2].set_yticklabels([])
        axICC[1,0].set_xlabel('')
        axICC[1,0].set_ylabel('MDC expressed as STD')
        axICC[1,1].set_xlabel('')
        axICC[1,1].set_ylabel('')
        axICC[1,2].set_xlabel('')
        axICC[1,2].set_ylabel('')
        axICC[1,0].set_title('')
        axICC[1,1].set_title('')
        axICC[1,2].set_title('')
        
    #    for label in axICC[1,0].xaxis.get_majorticklabels():
    #        label.set_transform(label.get_transform() + offset)
    #    for label in axICC[1,1].xaxis.get_majorticklabels():
    #        label.set_transform(label.get_transform() + offset)
    #    for label in axICC[1,2].xaxis.get_majorticklabels():
    #        label.set_transform(label.get_transform() + offset)
    #          
        # Spatio-Temporal features
        varNames = xlsFM.iloc[:,0]
        for number, value in enumerate(varNames):
            num = number+1
            varNames.iloc[number] = str(f'{num}. ' + value)
        
        tD = varNames[0:21]
        fD = varNames[21:29]
        cO  = varNames[29:35]
        
        labels = [item.get_text() for item in axICC[1,0].get_xticklabels()]
        
        labels[1] = ''
        
        labels[2:23] = tD
        labels[0] = ''
    #    labels[23] = ''
        
        axICC[1,0].set_xticklabels(labels,rotation = 45, ha = 'right',rotation_mode="anchor")
        
        
        # Frequency features
        labels = [item.get_text() for item in axICC[1,1].get_xticklabels()]
        
        labels[1:10] = fD
        labels[0] = ''
        #labels[] = ''
        #labels[23] = ''
        
        axICC[1,1].set_xticklabels(labels,rotation = 45, ha = 'right',rotation_mode="anchor")
        
        
        # Complexity features
        labels = [item.get_text() for item in axICC[1,2].get_xticklabels()]
        
        labels[2:8] = cO
        labels[0] = ''
        labels[1] = ''
        
        #labels[] = ''
        #labels[23] = ''
        
        axICC[1,2].set_xticklabels(labels, rotation = 45, ha = 'right',rotation_mode="anchor")
    
        os.chdir(saveTo)
        
        filename = afkorting + '.png'
        plt.savefig(filename, dpi = 600)
        os.chdir(mainDirectory)

if __name__ == '__main__':
    plotSIT()
    plotStanding()
