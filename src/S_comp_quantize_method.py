# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:41:45 2016

@author: My402
"""

import os
import numpy as np
from numpy import zeros,size
from function import BMR
from universal_statistical_test import Entropy
from security_sampling import sampling
from security_quantize import quantization_even,quantization_thre,remain
import matplotlib.pyplot as plt

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
ent = zeros((group_num,condi_num))

for i in range(group_num):
    print 'Running group:',i
    
    rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time,0.9,0.4)
    
    bitsA = quantization_even('RSSI',rssi_A,block_size,qtype,order)
    bitsB = quantization_even('RSSI',rssi_B,block_size,qtype,order)
    bmr[i,0] = BMR(bitsA,bitsB)
    bgr[i,0] = size(bitsA)/(sampling_time*1000.0/sampling_period)
    #ent[i,0] = Entropy(bitsA)
    
    bitsA = quantization_even('RSSI',rssi_A,size(rssi_A),qtype,order)
    bitsB = quantization_even('RSSI',rssi_B,size(rssi_A),qtype,order)
    bmr[i,1] = BMR(bitsA,bitsB)
    bgr[i,1] = size(bitsA)/(sampling_time*1000.0/sampling_period)
    #ent[i,1] = Entropy(bitsA)
    
    bitsA,drop_listA = quantization_thre(rssi_A,block_size,coef)
    bitsB,drop_listB = quantization_thre(rssi_B,block_size,coef)
    bitsA = remain(bitsA,drop_listA,drop_listB)
    bitsB = remain(bitsB,drop_listA,drop_listB)
    bmr[i,2] = BMR(bitsA,bitsB)
    bgr[i,2] = size(bitsA)/(sampling_time*1000.0/sampling_period)
    #ent[i,2] = Entropy(bitsA)
    
plt.figure(figsize=(8,5))
plt.plot(bmr[:,0],'ro-' ,label='Lightweight(%dbit %s,bl=%d)'%(order,qtype,block_size))
plt.plot(bmr[:,1],'go-' ,label='ASBG Multi(%dbit %s)'%(order,qtype))
plt.plot(bmr[:,2],'bo-' ,label='ASBG Single(coef=%.2f,bl=%d)'%(coef,block_size))
plt.legend()
plt.xlabel('Expriment')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different quantize methods')

plt.figure(figsize=(8,5))
plt.plot(bgr[:,0],'ro-' ,label='Lightweight(%dbit %s,bl=%d)'%(order,qtype,block_size))
plt.plot(bgr[:,1],'go-' ,label='ASBG Multi(%dbit %s)'%(order,qtype))
plt.plot(bgr[:,2],'bo-' ,label='ASBG Single(coef=%.2f,bl=%d)'%(coef,block_size))
plt.legend()
plt.xlabel('Expriment')
plt.ylabel('Bit Generation Rate')
plt.title('BGR of different quantize methods')

plt.figure(figsize=(8,5))
plt.plot(ent[:,0],'ro-' ,label='Lightweight(%dbit %s,bl=%d)'%(order,qtype,block_size))
plt.plot(ent[:,1],'go-' ,label='ASBG Multi(%dbit %s)'%(order,qtype))
plt.plot(ent[:,2],'bo-' ,label='ASBG Single(coef=%.2f,bl=%d)'%(coef,block_size))
plt.legend()
plt.xlabel('Expriment')
plt.ylabel('Entropy')
plt.title('Entropy of different quantize methods')
