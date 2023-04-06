"""
Created on Sun May 22, 2022

@author: Adam
"""

import mne
from mne.time_frequency import tfr_morlet, psd_multitaper, read_tfrs
import numpy as np

subjs = [12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52]


#Specify frequency bins
freq0 = [0,1,2] #Delta freqs
freq1 = [3,4,5,6] #Theta freqs
freq2 = [7,8] #alpha freqs
freq3 = [9,10,11] #beta
freq4 = [12,13] # Gamma 1
freq5 = [14,15,16,17] #Gamma 2


#Preallocate arrays separately by cue condition, time, and subsequent memory
TargSMEs_prestim = [[]]*len(subjs)
DistSMEs_prestim = [[]]*len(subjs)
TargSMEs_0to500 = [[]]*len(subjs)
DistSMEs_0to500 = [[]]*len(subjs)
TargSMEs_500to1000 = [[]]*len(subjs)
DistSMEs_500to1000 = [[]]*len(subjs)

TargRem_prestim = [[]]*len(subjs)
TargForg_prestim = [[]]*len(subjs)
DistRem_prestim = [[]]*len(subjs)
DistForg_prestim = [[]]*len(subjs)
TargRem_0to500 = [[]]*len(subjs)
TargForg_0to500 = [[]]*len(subjs)
DistRem_0to500 = [[]]*len(subjs)
DistForg_0to500 = [[]]*len(subjs)
TargRem_500to1000 = [[]]*len(subjs)
TargForg_500to1000 = [[]]*len(subjs)
DistRem_500to1000 = [[]]*len(subjs)
DistForg_500to1000 = [[]]*len(subjs)


#Cycle over participants
for  i in list(range(0, len(subjs))):
    print('Starting Subject '+str(i+1)+' of ' + str(len(subjs)))
    
    #Load data and specify distractor events
    aa = read_tfrs('/Volumes/experiments/abe/FR_EEG/Spectral_Density/PowerRem_16hz_ABE'+str(subjs[i])+'.fif')
    Remmd = aa[0].copy()
    Events = np.array(Remmd.info['events'][:, 2])
    Remmd.data = Remmd.data[Events == 48]
    Remmd.info['events'] = Remmd.info['events'][Events == 48]

    bb= read_tfrs('/Volumes/experiments/abe/FR_EEG/Spectral_Density/PowerForg_16hz_ABE_'+str(subjs[i])+'.fif')
    Forgd = bb[0].copy()
    Events = np.array(Forgd.info['events'][:, 2])
    Forgd.data = Forgd.data[Events == 48]
    Forgd.info['events'] = Forgd.info['events'][Events == 48]

    
    DistRemfreqs = [[[]]*6]*64
    DistForgfreqs = [[[]]*6]*64

    for j in list(range(0,64)):
        #Remembered events
        tempPow = []
        for t in list(range(0,6)): #loop through frequency bands
            freqs = globals()['freq%s' % t]
            RemPow = []
            for k in list(range(0, len(Remmd.data))): #loop through events
                RFP = []
                for r in list(range(0, len(freqs))): #loop through each frequency within a band
                    RFP.append(np.nanmean(Remmd.data[k][j][freqs[r]][0:9]))
                
                RemPow.append(np.mean(RFP))

            tempPow.append(np.nanmean(RemPow))#average frequencies within band
        DistRemfreqs[j] = tempPow #average frequency band power over events
    
            
    for j in list(range(0,64)):
        #Forgotten events
        tempPow = []
        for t in list(range(0,6)): #loop through frequency bands
            freqs = globals()['freq%s' % t]
            ForgPow = []
            for k in list(range(0, len(Forgd.data))): #loop through events
                FFP = []
                for r in list(range(0, len(freqs))): #loop through each frequency within a band
                    FFP.append(np.nanmean(Forgd.data[k][j][freqs[r]][0:9])) 

                ForgPow.append(np.mean(FFP))

            tempPow.append(np.nanmean(ForgPow))#average frequencies within band
        DistForgfreqs[j] = tempPow #average frequency band power over events
        


    temps2 = [[]]*64

    for j in list(range(0,64)):
        temps = []
        for t in list(range(0, 6)):
            temps.append(DistRemfreqs[j][t] - DistForgfreqs[j][t])
            
        temps2[j] = temps
    DistSMEs_prestim[i] = temps2
    DistRem_prestim[i] = DistRemfreqs
    DistForg_prestim[i] = DistForgfreqs
    
  
    

    
    #Specify Target events
    Remmd = aa[0].copy()
    Events = np.array(Remmd.info['events'][:, 2])
    Remmd.data = Remmd.data[Events == 49]
    Remmd.info['events'] = Remmd.info['events'][Events == 49]


    Forgd = bb[0].copy()
    Events = np.array(Forgd.info['events'][:, 2])
    Forgd.data = Forgd.data[Events == 49]
    Forgd.info['events'] = Forgd.info['events'][Events == 49]

    
    TargRemfreqs = [[[]]*6]*64
    TargForgfreqs = [[[]]*6]*64

    for j in list(range(0,64)):
        #Remembered events
        tempPow = []
        for t in list(range(0,6)): #loop through frequency bands
            freqs = globals()['freq%s' % t]
            RemPow = []
            for k in list(range(0, len(Remmd.data))): #loop through events
                RFP = []
                for r in list(range(0, len(freqs))): #loop through each frequency within a band
                    RFP.append(np.nanmean(Remmd.data[k][j][freqs[r]][0:9])) 

                RemPow.append(np.mean(RFP))

            tempPow.append(np.nanmean(RemPow))#average frequencies within band
        TargRemfreqs[j] = tempPow #average frequency band power over events
    
            
    for j in list(range(0,64)):
        #Forgotten events
        tempPow = []
        for t in list(range(0,6)): #loop through frequency bands
            freqs = globals()['freq%s' % t]
            ForgPow = []
            for k in list(range(0, len(Forgd.data))): #loop through events
                FFP = []
                for r in list(range(0, len(freqs))): #loop through each frequency within a band
                    FFP.append(np.nanmean(Forgd.data[k][j][freqs[r]][0:9])) 

                ForgPow.append(np.mean(FFP))
            tempPow.append(np.nanmean(ForgPow))#average frequencies within band
        TargForgfreqs[j] = tempPow #average frequency band power over events
        


    temps2 = [[]]*64

    for j in list(range(0,64)):
        temps = []
        for t in list(range(0, 6)):
            temps.append(TargRemfreqs[j][t] - TargForgfreqs[j][t])
            
        temps2[j] = temps
    TargSMEs_prestim[i] = temps2
    TargRem_prestim[i] = TargRemfreqs
    TargForg_prestim[i] = TargForgfreqs
    
    
    Remmd = aa[0].copy()
    Events = np.array(Remmd.info['events'][:, 2])
    Remmd.data = Remmd.data[Events == 48]
    Remmd.info['events'] = Remmd.info['events'][Events == 48]
    
    
    Forgd = bb[0].copy()
    Events = np.array(Forgd.info['events'][:, 2])
    Forgd.data = Forgd.data[Events == 48]
    Forgd.info['events'] = Forgd.info['events'][Events == 48]
                     
                    
    DistRemfreqs = [[[]]*6]*64
    DistForgfreqs = [[[]]*6]*64
    
    for j in list(range(0,64)):
        #Remembered events
        tempPow = []
        for t in list(range(0,6)): #loop through frequency bands
            freqs = globals()['freq%s' % t]
            RemPow = []
            for k in list(range(0, len(Remmd.data))): #loop through events
                RFP = []
                for r in list(range(0, len(freqs))): #loop through each frequency within a band
                    RFP.append(np.nanmean(Remmd.data[k][j][freqs[r]][9:17])) 

                RemPow.append(np.mean(RFP))

            tempPow.append(np.nanmean(RemPow))#average frequencies within band
        DistRemfreqs[j] = tempPow #average frequency band power over events
    
            
    for j in list(range(0,64)):
        #Forgotten events
        tempPow = []
        for t in list(range(0,6)): #loop through frequency bands
            freqs = globals()['freq%s' % t]
            ForgPow = []
            for k in list(range(0, len(Forgd.data))): #loop through events
                FFP = []
                for r in list(range(0, len(freqs))): #loop through each frequency within a band
                    FFP.append(np.nanmean(Forgd.data[k][j][freqs[r]][9:17])) 
                ForgPow.append(np.mean(FFP))
     
            tempPow.append(np.nanmean(ForgPow))#average frequencies within band
        DistForgfreqs[j] = tempPow #average frequency band power over events
        
    
    
    temps2 = [[]]*64
    
    for j in list(range(0,64)):
        temps = []
        for t in list(range(0, 6)):
            temps.append(DistRemfreqs[j][t] - DistForgfreqs[j][t])
            
        temps2[j] = temps
    DistSMEs_0to500[i] = temps2
    DistRem_0to500[i] = DistRemfreqs
    DistForg_0to500[i] = DistForgfreqs
    
    
    
    
    
    Remmd = aa[0].copy()
    Events = np.array(Remmd.info['events'][:, 2])
    Remmd.data = Remmd.data[Events == 49]
    Remmd.info['events'] = Remmd.info['events'][Events == 49]
    
    
    Forgd = bb[0].copy()
    Events = np.array(Forgd.info['events'][:, 2])
    Forgd.data = Forgd.data[Events == 49]
    Forgd.info['events'] = Forgd.info['events'][Events == 49]
    
    
    TargRemfreqs = [[[]]*6]*64
    TargForgfreqs = [[[]]*6]*64
    
    for j in list(range(0,64)):
        #Remembered events
        tempPow = []
        for t in list(range(0,6)): #loop through frequency bands
            freqs = globals()['freq%s' % t]
            RemPow = []
            for k in list(range(0, len(Remmd.data))): #loop through events
                RFP = []
                for r in list(range(0, len(freqs))): #loop through each frequency within a band
                    RFP.append(np.nanmean(Remmd.data[k][j][freqs[r]][9:17])) 
                
                RemPow.append(np.mean(RFP))

            tempPow.append(np.nanmean(RemPow))#average frequencies within band
        TargRemfreqs[j] = tempPow #average frequency band power over events
    
            
    for j in list(range(0,64)):
        #Forgotten events
        tempPow = []
        for t in list(range(0,6)): #loop through frequency bands
            freqs = globals()['freq%s' % t]
            ForgPow = []
            for k in list(range(0, len(Forgd.data))): #loop through events
                FFP = []
                for r in list(range(0, len(freqs))): #loop through each frequency within a band
                    FFP.append(np.nanmean(Forgd.data[k][j][freqs[r]][9:17])) 
                ForgPow.append(np.mean(FFP))
            tempPow.append(np.nanmean(ForgPow))#average frequencies within band
        TargForgfreqs[j] = tempPow #average frequency band power over events
        
    
    
    temps2 = [[]]*64
    
    for j in list(range(0,64)):
        temps = []
        for t in list(range(0, 6)):
            temps.append(TargRemfreqs[j][t] - TargForgfreqs[j][t])
            
        temps2[j] = temps
    TargSMEs_0to500[i] = temps2
    TargRem_0to500[i] = TargRemfreqs
    TargForg_0to500[i] = TargForgfreqs
    
    
    Remmd = aa[0].copy()
    Events = np.array(Remmd.info['events'][:, 2])
    Remmd.data = Remmd.data[Events == 48]
    Remmd.info['events'] = Remmd.info['events'][Events == 48]
    
    
    Forgd = bb[0].copy()
    Events = np.array(Forgd.info['events'][:, 2])
    Forgd.data = Forgd.data[Events == 48]
    Forgd.info['events'] = Forgd.info['events'][Events == 48]
                        

    DistRemfreqs = [[[]]*6]*64
    DistForgfreqs = [[[]]*6]*64
    
    for j in list(range(0,64)):
        #Remembered events
        tempPow = []
        for t in list(range(0,6)): #loop through frequency bands
            freqs = globals()['freq%s' % t]
            RemPow = []
            for k in list(range(0, len(Remmd.data))): #loop through events
                RFP = []
                for r in list(range(0, len(freqs))): #loop through each frequency within a band
                    RFP.append(np.nanmean(Remmd.data[k][j][freqs[r]][17:25])) 

                RemPow.append(np.mean(RFP))

            tempPow.append(np.nanmean(RemPow))#average frequencies within band
        DistRemfreqs[j] = tempPow #average frequency band power over events
    
            
    for j in list(range(0,64)):
        #Forgotten events
        tempPow = []
        for t in list(range(0,6)): #loop through frequency bands
            freqs = globals()['freq%s' % t]
            ForgPow = []
            for k in list(range(0, len(Forgd.data))): #loop through events
                FFP = []
                for r in list(range(0, len(freqs))): #loop through each frequency within a band
                    FFP.append(np.nanmean(Forgd.data[k][j][freqs[r]][17:25])) 

                ForgPow.append(np.mean(FFP))
            tempPow.append(np.nanmean(ForgPow))#average frequencies within band
        DistForgfreqs[j] = tempPow #average frequency band power over events
        
    
    
    temps2 = [[]]*64
    
    for j in list(range(0,64)):
        temps = []
        for t in list(range(0, 6)):
            temps.append(DistRemfreqs[j][t] - DistForgfreqs[j][t])
            
        temps2[j] = temps
    DistSMEs_500to1000[i] = temps2
    DistRem_500to1000[i] = DistRemfreqs
    DistForg_500to1000[i] = DistForgfreqs
    
    
    
    
    
    Remmd = aa[0].copy()
    Events = np.array(Remmd.info['events'][:, 2])
    Remmd.data = Remmd.data[Events == 49]
    Remmd.info['events'] = Remmd.info['events'][Events == 49]
    
    
    Forgd = bb[0].copy()
    Events = np.array(Forgd.info['events'][:, 2])
    Forgd.data = Forgd.data[Events == 49]
    Forgd.info['events'] = Forgd.info['events'][Events == 49]
    
    
    TargRemfreqs = [[[]]*6]*64
    TargForgfreqs = [[[]]*6]*64
    
    for j in list(range(0,64)):
        #Remembered events
        tempPow = []
        for t in list(range(0,6)): #loop through frequency bands
            freqs = globals()['freq%s' % t]
            RemPow = []
            for k in list(range(0, len(Remmd.data))): #loop through events
                RFP = []
                for r in list(range(0, len(freqs))): #loop through each frequency within a band
                    RFP.append(np.nanmean(Remmd.data[k][j][freqs[r]][17:25])) 

                RemPow.append(np.mean(RFP))

            tempPow.append(np.nanmean(RemPow))#average frequencies within band
        TargRemfreqs[j] = tempPow #average frequency band power over events
    
            
    for j in list(range(0,64)):
        #Forgotten events
        tempPow = []
        for t in list(range(0,6)): #loop through frequency bands
            freqs = globals()['freq%s' % t]
            ForgPow = []
            for k in list(range(0, len(Forgd.data))): #loop through events
                FFP = []
                for r in list(range(0, len(freqs))): #loop through each frequency within a band
                    FFP.append(np.nanmean(Forgd.data[k][j][freqs[r]][17:25])) 

                ForgPow.append(np.mean(FFP))

            tempPow.append(np.nanmean(ForgPow))#average frequencies within band
        TargForgfreqs[j] = tempPow #average frequency band power over events
        
    
    
    temps2 = [[]]*64
    
    for j in list(range(0,64)):
        temps = []
        for t in list(range(0, 6)):
            temps.append(TargRemfreqs[j][t] - TargForgfreqs[j][t])
            
        temps2[j] = temps
    TargSMEs_500to1000[i] = temps2
    TargRem_500to1000[i] = TargRemfreqs
    TargForg_500to1000[i] = TargForgfreqs
    
    