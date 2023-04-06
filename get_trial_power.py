#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 15:04:33 2020

@author: Adam
"""

import statistics
import mne
import numpy as np
from mne.time_frequency import tfr_morlet, psd_multitaper
#subjs = [34,37,40,41,43,46,47,49,54]


def run(epochs):
    freqs = np.logspace(*np.log10([2, 100]), num=18)
    n_cycles = freqs/2.
    chans = list(range(0,64))#[4, 5, 6, 8, 9, 10, 17,30,31,33,34,35, 37, 38, 39, 21, 42, 43, 45, 49,50,62,63,65,66,67,74,75,87,88,97,98,99,107, 125, 126, 127]
    Power = tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles,
                  decim = 32, picks = chans, return_itc=False, average = False)
    Power.info['events'] = epochs.events
    return Power