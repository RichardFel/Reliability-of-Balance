import numpy as np
from visualise import Visualisation

class Complexity: 

    def statespace(signal, ndim = 5, delay = 10):
        try:
            m,n = signal.shape
            state = np.zeros((m - delay * (ndim ), ndim,n))
    
        except ValueError:
            m = len(signal)
            state = np.zeros((m - delay * (ndim ), ndim,1))
            
        for i_dim in range(ndim):          
            state[:,i_dim,:] = signal[i_dim*delay:len(signal)-(ndim - i_dim) * delay]
         
        return state   
        # State is a ndim x normalised length x n matrix
        
            
    def rosenstein(lowBack, state, period = 1, ws = 0.5, nnbs = 5, plot = None):
        # ws: wiundow size over which divergence should be calculated
        # fs: sample frequentie
        try:
            fs = lowBack.new_sf
        except AttributeError:
            fs = int(1 / lowBack.sampleFreq)
            
        m,n,o = state.shape    
        ws = int(ws * fs)
        emptyarray = np.empty((ws,n,o))
        emptyarray[:] = np.nan
        state = np.concatenate((state, emptyarray),axis = 0) #we extend the state space with NaN, so that we don't run into problems later
        L1 = 0.5 * period * fs
        divergence = np.zeros((m*nnbs,ws,o))
        difference = np.zeros((m+ws,n,o))
        lde = np.zeros(o)
        
        for i_t in range(0,o):
            counter = 0
            for i in range(0,m): # loop over time samples
                for j in range(0,n): # loop over dimensions -> Efficienter
                    difference[:,j,i_t] = np.subtract(state[:,j,i_t],state[i,j,i_t]) ** 2
                    
                start_index         = int(np.max([0,i-int(0.5*fs*period)])) #find point half a period befor current point   
                stop_index          = int(np.min([m,i+int(0.5*fs*period)])) #find point half a period past current point     
                difference[start_index:stop_index,:,i_t] = np.nan# discard data within one period from sample i_t putting it to n an            
                index          = np.sum(difference[:,:,i_t],axis = 1).argsort()
                
                for k in range(0,nnbs):
                    div_tmp = np.subtract(state[i:i+ws,:,i_t],state[index[k]:index[k]+ws,:,i_t])
                    divergence[counter,:,i_t] =  np.sqrt(np.sum(div_tmp**2,axis = 1)) 
                    counter += 1 
                    
            divmat =np.nanmean(np.log(divergence[:,:,i_t]),0); # calculate average for output      
            xdiv =  np.linspace(1,len(divmat), num = int(0.5*fs*period))
            Ps = np.polynomial.polynomial.polyfit(xdiv, divmat[0:int(np.floor(L1))],1)
                
            sfit = np.polynomial.Polynomial(Ps)
            lde[i_t] = Ps[1]
            
        
            if plot:
                Visualisation.plot3(divmat, sfit(xdiv),title = 'Lyapunov Rosenstein' ,
                                     xlabel = 'time [s]', ylabel = 'divergence',
                                     legend1 = 'divergence', legend2 = 'lde short'
                                     )
                
        return divergence, lde[0]
    
    
    def count_vectors(m, r, N, signal):
        C = np.zeros((len(signal)-m +1,1))
        for i in range(N-(m-1)):
            tmpSignal = signal[i:]
            checkValues = tmpSignal
            for j in range(m):
                refValue = signal[i+j]
                minVal = refValue - r
                maxVal = refValue + r
                matchesIDX = np.where((checkValues >= minVal) 
                                        & (checkValues <= maxVal))[0]
                if j == 0:
                    initmatchesIDX = matchesIDX
                    folNumbIDX = matchesIDX + 1
                else:
                    initmatchesIDX = initmatchesIDX[matchesIDX]
                    folNumbIDX = initmatchesIDX + 1 + j
                try:
                    checkValues = tmpSignal[folNumbIDX]
                except IndexError: 
                    checkValues = tmpSignal[folNumbIDX[:-1]]
                    
            C[i] += len(matchesIDX)    
            
            try:
                C[(folNumbIDX[1:]-1 - j + i)] += 1
            except:
                continue
            
        return C
    
    def aproximateEntropy(m, r, signal):
        m_2 = m + 1
        N = len(signal)

        firstResult = Complexity.count_vectors(m, r, N, signal)
        logFR = np.sum(np.log(firstResult/ (N - m + 1)))
        phi = logFR / (N - m + 1)
        
        secondResult = Complexity.count_vectors(m_2, r, N, signal)
        logSR = np.sum(np.log(secondResult / (N - m)))
        phi_2 = logSR / (N - m)
        
        entropy = phi - phi_2
        return entropy
    
    
    def sampleEntropy(m, r, signal):
        m_2 = m + 1
        N = len(signal)
     
        firstResult = Complexity.count_vectors(m, r, N, signal) - 1 
        logFR = np.sum((firstResult / (N - m))) / (N- m)
        phi = logFR * (( (N-m - 1)* (N-m)) / 2)
        
        secondResult = Complexity.count_vectors(m_2, r, N, signal) - 1
        logSR = np.sum(secondResult / (N - m_2))  / (N- m)
        phi_2 = logSR * (( (N-m - 1)* (N-m)) / 2)
        
        entropy =  -np.log( phi_2 /phi) # Returns values between 0 and 2
        return entropy
            

