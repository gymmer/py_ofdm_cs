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
from RSSI import sampling,quantization_thre,remain 
from part_transmission import awgn
from winnow import winnow
import matplotlib.pyplot as plt

os.system('cls')
plt.close('all')

sampling_period = 1     # 采样周期1ms
sampling_time = 40
SNR = 30
block_size = 200
coef = 0.4
interation = [0,1,2,3,4]

group_num = 1
condi_num = size(interation)
bmr = zeros((group_num,condi_num))
bgr = zeros((group_num,condi_num))
ent = zeros((group_num,condi_num))

for i in range(group_num):
    for j in range(condi_num):
        print 'Running group:',i,j
        
        rssi_A = sampling(sampling_period,sampling_time,3)
        rssi_B = awgn(rssi_A,SNR)
    
        bitsA,drop_listA = quantization_thre(rssi_A,block_size,coef)
        bitsB,drop_listB = quantization_thre(rssi_B,block_size,coef)
        bitsA = remain(bitsA,drop_listA,drop_listB)
        bitsB = remain(bitsB,drop_listA,drop_listB)
        bitsA,bitsB = winnow(bitsA,bitsB,interation[j])
        
        bmr[i,j] = BMR(bitsA,bitsB)
        bgr[i,j] = size(bitsA)/(sampling_time/sampling_period*1000.0)
        ent[i,j] = Entropy(bitsA)

bmr = mean(bmr,0)
bgr = mean(bgr,0)
ent = mean(ent,0)

plt.figure(figsize=(8,5))
plt.plot(interation,bmr,'bo-')
plt.xlabel('Interation')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different interation of winnow(bl=%d,coef=%.2f)'%(block_size,coef))

plt.figure(figsize=(8,5))
plt.plot(interation,bgr,'bo-')
plt.xlabel('Interation')
plt.ylabel('Bit Generate Rate')
plt.title('BGR of different interation of winnow(bl=%d,coef=%.2f)'%(block_size,coef))
plt.ylim(0,1)

plt.figure(figsize=(8,5))
plt.plot(interation,ent,'bo-')
plt.xlabel('Interation')
plt.ylabel('Entropy')
plt.title('Entropy of different interation of winnow(bl=%d,coef=%.2f)'%(block_size,coef))
plt.ylim(0,1)
