# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:41:45 2016

@author: My402
"""

import os
import numpy as np
from numpy import zeros,size,mean
from function import BMR
from universal_statistical_test import Entropy
from RSSI_sampling import sampling
from RSSI_quantization import quantization_thre,remain
from part_transmission import awgn
import matplotlib.pyplot as plt

os.system('cls')
plt.close('all')

sampling_period = 1     # 采样周期1ms
sampling_time = 30
SNR = 30
block_size = 25
coef = [i/10.0 for i in range(10)]

group_num = 1
condi_num = size(coef)
bmr = zeros((group_num,condi_num))
bgr = zeros((group_num,condi_num))
ent = zeros((group_num,condi_num))

for i in range(group_num):
    for j in range(condi_num):
        print 'Running group:',i,j
        
        rssi_A = sampling(sampling_period,sampling_time,3)
        rssi_B = awgn(rssi_A,SNR)
    
        bitsA,drop_listA = quantization_thre(rssi_A,block_size,coef[j])
        bitsB,drop_listB = quantization_thre(rssi_B,block_size,coef[j])
        bitsA = remain(bitsA,drop_listA,drop_listB)
        bitsB = remain(bitsB,drop_listA,drop_listB)
        
        bmr[i,j] = BMR(bitsA,bitsB)
        bgr[i,j] = size(bitsA)/(sampling_time/sampling_period*1000.0)
        ent[i,j] = Entropy(bitsA)

bmr = mean(bmr,0)
bgr = mean(bgr,0)
ent = mean(ent,0)

plt.figure(figsize=(8,5))
plt.plot(coef,bmr,'bo-')
plt.xlabel('Coefficient')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different coef in thresold method(bl=%d)'%(block_size))

plt.figure(figsize=(8,5))
plt.plot(coef,bgr,'bo-')
plt.xlabel('Coefficient')
plt.ylabel('Bit Generate Rate')
plt.title('BGR of different coef in thresold method(bl=%d)'%(block_size))

plt.figure(figsize=(8,5))
plt.plot(coef,ent,'bo-')
plt.xlabel('Coefficient')
plt.ylabel('Entropy')
plt.title('Entropy of different coef in thresold method(bl=%d)'%(block_size))
