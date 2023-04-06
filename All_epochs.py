#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri 12 Nov. 2021

@author: Adam Broitman
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import statistics
import pandas
import mne
import pickle
import numpy as np
import csv


def run(subj):

    data_path = '/Volumes/experiments/abe/FR_EEG/preprocessed_EEG/'
    
    excl = ["EXG1", "EXG2", "EXG3", "EXG4", "EXG5", "EXG6", "EXG7", "EXG8"]
    

    filename = data_path+'NoDetect_'+str(subj)+'.fif'
    raw = mne.io.read_raw_fif(filename, preload=True)


    picks = mne.pick_types(raw.info, eeg=True, eog=False, stim=False, exclude=excl)
    events = mne.find_events(raw)
    
    epochs = mne.Epochs(raw, events, picks=picks, event_id= [48, 49], tmin=-0.7, tmax=1.2, preload=True)

    

    
#    with open(str(subj)+'_remembered', newline='') as csvfile:
#        Remmd =list(csv.reader(csvfile))
#    with open(str(subj)+'_forgotten', newline='') as csvfile:
#        Forggd =list(csv.reader(csvfile))
    forgd = pandas.read_csv('/Users/Adam/Documents/Adam_Python/ABE_FR_EEG/Rem_Forg/Forg_'+str(subj)+'.txt', sep = "\t")
    remmd = pandas.read_csv('/Users/Adam/Documents/Adam_Python/ABE_FR_EEG/Rem_Forg/Remmd_'+str(subj)+'.txt', sep = "\t")
    Forggd = np.array(forgd.F)
    Remmd = np.array(remmd.R)
    Remembered = []
    for k in list(range(0, len(Remmd))):
        Remembered.append(int(Remmd[k]) - 1)
    Forgotten = []
    for k in list(range(0, len(Forggd))):
        Forgotten.append(int(Forggd[k]) - 1)
        
    return epochs, Remembered, Forgotten
    

#for j in list(range(1, len(subjs))):
#    all_Rem = mne.concatenate_epochs([all_Rem, globals()['epochs_rem' + str(subjs[j])]])
#    all_Forg = mne.concatenate_epochs([all_Forg, globals()['epochs_forg' + str(subjs[j])]])
#    all_Remtarg = mne.concatenate_epochs([all_Remtarg, globals()['epochs_remtarg' + str(subjs[j])]])
#    all_Forgtarg = mne.concatenate_epochs([all_Forgtarg, globals()['epochs_forgtarg' + str(subjs[j])]])
#    all_Remdist = mne.concatenate_epochs([all_Remdist, globals()['epochs_remdist' + str(subjs[j])]])
#    all_Forgdist = mne.concatenate_epochs([all_Forgdist, globals()['epochs_forgdist' + str(subjs[j])]])
