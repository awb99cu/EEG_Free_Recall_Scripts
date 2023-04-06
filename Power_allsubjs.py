
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 16:56:00 2020

@author: Adam
"""

import All_epochs
import get_trial_power
import Ztrans_power
import mne
from mne.time_frequency import tfr_morlet, psd_multitaper

#subjs = [12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52]
subjs = [2,4,5,6,7,8,9,10,11,53,54,55,56,57,58,59,60,61,62,63,64]

for  i in list(range(0, len(subjs))):
    print('Starting Subject '+str(i+1)+' of ' + str(len(subjs)))
    epochs, Remembered, Forgotten = All_epochs.run(subjs[i])
    power = get_trial_power.run(epochs)
    power.crop(tmin = -.5, tmax = 1)
    Zpower, Power_Rem, Power_Forg = Ztrans_power.run(power, Remembered, Forgotten)
    Zpower.save('/Volumes/experiments/abe/FR_EEG/Spectral_Density//Power_16hz_'+str(subjs[i])+'.fif', overwrite = True)
    Power_Rem.save('/Volumes/experiments/abe/FR_EEG/Spectral_Density//PowerRem_16hz_NoDetect_'+str(subjs[i])+'.fif', overwrite = True)
    Power_Forg.save('/Volumes/experiments/abe/FR_EEG/Spectral_Density//PowerForg_16hz_NoDetect_'+str(subjs[i])+'.fif', overwrite = True)
    