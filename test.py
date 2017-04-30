# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:41:45 2016

@author: My402
"""

import os
import numpy as np
from numpy import zeros
from function import BMR
from RSSI_sampling import sampling
from RSSI_quantization import quantization_even,quantization_thre,remain
from part_transmission import awgn
import matplotlib.pyplot as plt

os.system('cls')
plt.close('all')

sampling_period = 1     # 采样周期1ms
sampling_time = 20
SNR = 30
block_size = 25


    
rssi_A = sampling(sampling_period,sampling_time,1)
rssi_B = awgn(rssi_A,SNR)
rssi_E = sampling(sampling_period,sampling_time,3)
    
print np.corrcoef(rssi_A,rssi_B,rowvar=0)
print np.corrcoef(rssi_A,rssi_E,rowvar=0)

bitsA,drop_listA = quantization_thre(rssi_A,block_size,0)
bitsB,drop_listB = quantization_thre(rssi_B,block_size,0)
bitsE,drop_listE = quantization_thre(rssi_E,block_size,0)
print BMR(bitsA,bitsB)
print BMR(bitsA,bitsE)
