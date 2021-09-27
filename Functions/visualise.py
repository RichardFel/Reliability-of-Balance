import numpy as np
import matplotlib.pyplot as plt

class Visualisation:  
    def plot1(signal, title = '', xlabel = '', ylabel = '', ylim = None):                                       # 3 subplots
        fig1, ax2 = plt.subplots(3)
        ax2[0].plot(np.array(range(0,len(signal))), signal[:,0]) 
        ax2[1].plot(np.array(range(0,len(signal))), signal[:,1]) 
        ax2[2].plot(np.array(range(0,len(signal))), signal[:,2]) 
        ax2[0].set_title(title)
        ax2[2].set_xlabel(xlabel)
        ax2[0].set_ylabel('VT')
        ax2[1].set_ylabel('ML')
        ax2[2].set_ylabel('AP')
        if ylim:
            ax2[0].set_ylim(-0.02, 0.02)
            ax2[1].set_ylim(-0.02, 0.02)
            ax2[2].set_ylim(-0.02, 0.02)
        
    def plot2(signal1, signal2, title, xlabel, ylabel1, ylabel2):                   # 2 subplots 
        fig1, ax2 = plt.subplots(2)
        ax2[0].plot(np.array(range(0,len(signal1))), signal1) 
        ax2[1].plot(np.array(range(0,len(signal2))), signal2) 
        ax2[0].set_title(title)
        ax2[1].set_xlabel(xlabel)
        ax2[0].set_ylabel(ylabel1)
        ax2[1].set_ylabel(ylabel2)
        
    def plot3(signal1, signal2, title, xlabel, ylabel, legend1, legend2):           # 1 plot 2 signals
        fig1, ax2 = plt.subplots()
        ax2.plot(np.array(range(0,len(signal1))), signal1 ) 
        ax2.plot(np.array(range(0,len(signal2))), signal2) 
        ax2.legend((legend1, legend2), loc='upper right')
        ax2.set_title(title)
        ax2.set_xlabel(xlabel)
        ax2.set_ylabel(ylabel)
        
    def plot4(signal, title = '', xlabel = '', ylabel = ''):                                       # 1 plot 
        fig1, ax2 = plt.subplots()
        ax2.plot(np.array(range(0,len(signal))), signal) 
        ax2.set_title(title)
        ax2.set_xlabel(xlabel)
        ax2.set_ylabel(ylabel)
    
    def plot5(signal1, signal2, signal3, title, xlabel, ylabel, legend1, legend2, legend3):           # 1 plot 3 signals
        fig1, ax2 = plt.subplots()
        ax2.plot(np.array(range(0,len(signal1))), signal1 ) 
        ax2.plot(np.array(range(0,len(signal2))), signal2) 
        ax2.plot(np.array(range(0,len(signal3))), signal3) 
    
        ax2.legend((legend1, legend2, legend3), loc='upper right')
        ax2.set_title(title)
        ax2.set_xlabel(xlabel)
        ax2.set_ylabel(ylabel)
        
    def plot6(signalx, signaly, title = '', xlabel = '', ylabel = '', ylim = None):                                       # 1 plot 
        fig1, ax2 = plt.subplots()
        ax2.plot(signalx, signaly) 
        ax2.set_title(title)
        ax2.set_xlabel(xlabel)
        ax2.set_ylabel(ylabel)   
        if ylim:
            ax2.set_ylim(0, 0.1)