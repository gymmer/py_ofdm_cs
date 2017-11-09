# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:41:45 2016

@author: My402
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from numpy import zeros,size,mean
from function import BMR,BGR
from security_sampling import sampling
from security_quantize import quantization_thre,remain 

os.system('cls')
plt.close('all')

sampling_period = 1     # 采样周期1ms
sampling_time = 3
block_size = 25
coef = [i/10.0 for i in range(10)]

group_num = 100
coef_num  = size(coef)
bmr = zeros((group_num,coef_num))
bgr = zeros((group_num,coef_num))

for i in range(group_num):
    for j in range(coef_num):
        print 'Running group:',i,j
    
        rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time,0.9,0.4)        
        bitsA,drop_listA = quantization_thre(rssi_A,block_size,coef[j])
        bitsB,drop_listB = quantization_thre(rssi_B,block_size,coef[j])
        bitsA = remain(bitsA,drop_listA,drop_listB)
        bitsB = remain(bitsB,drop_listA,drop_listB)
                   
        bmr[i,j] = BMR(bitsA,bitsB)
        bgr[i,j] = BGR(bitsA,sampling_time,sampling_period)

bmr = mean(bmr,0)
bgr = mean(bgr,0)

plt.figure(figsize=(8,5))
plt.plot(coef,bmr,'bo-')
plt.xlabel('Coefficient')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different coef(bl=%d)'%(block_size))
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(coef,bgr,'bo-')
plt.xlabel('Coefficient')
plt.ylabel('Bit Generate Rate')
plt.title('BGR of different coef(bl=%d)'%(block_size))
plt.legend()
plt.ylim(0,1)
