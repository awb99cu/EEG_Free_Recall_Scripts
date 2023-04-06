#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 14:53:24 2021

@author: Adam
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 15:37:24 2020

@author: Adam
"""
import mne
from mne.time_frequency import tfr_morlet, psd_multitaper
import numpy as np
def run(Power, Remembered, Forgotten):
    tempPow = Power.data
    for i in list(range(0, len(Power.data[0]))): # for each channel
        for k in list(range(0, len(Power.data[0][0]))): # for each frequency 
            power_raw = []
            for j in list(range(0, len(Power.data))): #For each epoch
                power_raw = power_raw + list(Power.data[j][i][k])
            Power_mean = np.mean(power_raw)
            power_std = np.std(power_raw)
            for j in list(range(0, len(Power.data))): #For each epoch
                tempPow[j][i][k] = (Power.data[j][i][k] - Power_mean)/power_std
                
    for i in list(range(0, len(Power.data[0]))): # for each channel
        for k in list(range(0, len(Power.data[0][0]))): # for each frequency 
            power_raw = []
            for j in list(range(0, len(Power.data))): #For each epoch
                if np.all(abs(tempPow[j][i][k]) < 3):
                    power_raw = power_raw + list(Power.data[j][i][k])
            Power_mean = np.nanmean(power_raw)
            power_std = np.nanstd(power_raw)
            for j in list(range(0, len(Power.data))): #For each epoch
                if np.all(abs(tempPow[j][i][k]) < 3):
                    Power.data[j][i][k] = (Power.data[j][i][k] - Power_mean)/power_std
                else:
                    Power.data[j][i][k] = np.array([np.nan for l in range(len(Power.data[j][i][k]))])
                
    
    Rem_pwr = Power.copy()
    Rem_pwr.data = Power.data[Remembered][:][:]
    Rem_pwr.info['events'] = Power.info['events'][Remembered]
    Forg_pwr = Power.copy()
    Forg_pwr.data = Power.data[Forgotten][:][:]
    Forg_pwr.info['events'] = Power.info['events'][Forgotten]

    return Power, Rem_pwr, Forg_pwr