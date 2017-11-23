# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:41:45 2016

@author: My402
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from numpy import zeros,size
from function import BMR,BGR
from security_sampling import sampling
from security_quantize import quantization_even,quantization_thre,remain

os.system('cls')
plt.close('all')

sampling_period = 1     # 采样周期1ms
sampling_time = 3
qtype = 'gray'
order = 2
block_size = 25
coef = 0.8

group_num = 10
condi_num = 3
bmr = zeros((group_num,condi_num))
bgr = zeros((group_num,condi_num))

for i in range(group_num):
    print 'Running group:',i
    
    rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time,0.9,0.4)
    
    bits_A = quantization_even('RSSI',rssi_A,block_size,qtype,order)
    bits_B = quantization_even('RSSI',rssi_B,block_size,qtype,order)
    bmr[i,0] = BMR(bits_A,bits_B)
    bgr[i,0] = BGR(bits_A,sampling_time,sampling_period)
    
    bits_A = quantization_even('RSSI',rssi_A,size(rssi_A),qtype,order)
    bits_B = quantization_even('RSSI',rssi_B,size(rssi_A),qtype,order)
    bmr[i,1] = BMR(bits_A,bits_B)
    bgr[i,1] = BGR(bits_A,sampling_time,sampling_period)
    
    bits_A,drop_list_A = quantization_thre(rssi_A,block_size,coef)
    bits_B,drop_list_B = quantization_thre(rssi_B,block_size,coef)
    bits_A = remain(bits_A,drop_list_A,drop_list_B)
    bits_B = remain(bits_B,drop_list_A,drop_list_B)
    bmr[i,2] = BMR(bits_A,bits_B)
    bgr[i,2] = BGR(bits_A,sampling_time,sampling_period)
    
plt.figure(figsize=(8,5))
plt.plot(bmr[:,0],'ro-',label='Lightweight(%dbit %s,bl=%d)'%(order,qtype,block_size))
plt.plot(bmr[:,1],'go-',label='ASBG Multi(%dbit %s)'%(order,qtype))
plt.plot(bmr[:,2],'bo-',label='ASBG Single(coef=%.2f,bl=%d)'%(coef,block_size))
plt.legend()
plt.xlabel('Expriment')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different quantize methods')

plt.figure(figsize=(8,5))
plt.plot(bgr[:,0],'ro-',label='Lightweight(%dbit %s,bl=%d)'%(order,qtype,block_size))
plt.plot(bgr[:,1],'go-',label='ASBG Multi(%dbit %s)'%(order,qtype))
plt.plot(bgr[:,2],'bo-',label='ASBG Single(coef=%.2f,bl=%d)'%(coef,block_size))
plt.legend()
plt.xlabel('Expriment')
plt.ylabel('Bit Generation Rate')
plt.title('BGR of different quantize methods')
