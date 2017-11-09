# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:41:45 2016

@author: My402
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from numpy import zeros,size,mean,mod,pi
from function import BMR,BGR
from security_sampling import sampling
from security_quantize import quantization_thre,quantization_even,remain
from security_winnow import winnow
from security_merge import merge

os.system('cls')
plt.close('all')

''' 采样参数 '''
sampling_period  = 1
sampling_time = 3

''' 量化参数 '''
block_size = 25
coef = 0.8
qtype = 'gray'
order = 1
mtype = 'cross'

iteration = [0,1,2,3,4]

group_num = 100
inter_num = size(iteration)
bmr = zeros((group_num,inter_num))
bgr = zeros((group_num,inter_num))

for i in range(group_num):
    for j in range(inter_num):
        print 'Running group:',i,j
        
        ''' 采样 ''' 
        rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time,0.9,0.4)  
        phase_A,phase_B,phase_E = mod(sampling('Phase',sampling_period,sampling_time,0.9,0.4),2*pi)
            
        ''' RSSI量化 '''
        bits_A_rssi,drop_listA = quantization_thre(rssi_A,block_size,coef)
        bits_B_rssi,drop_listB = quantization_thre(rssi_B,block_size,coef)
        bits_A_rssi = remain(bits_A_rssi,drop_listA,drop_listB)
        bits_B_rssi = remain(bits_B_rssi,drop_listA,drop_listB)
        
        ''' Phase量化 '''
        bits_A_phase = quantization_even('Phase',phase_A,size(phase_A),qtype,order)
        bits_B_phase = quantization_even('Phase',phase_B,size(phase_B),qtype,order)
        
        ''' 合并 '''
        bits_A = merge(bits_A_rssi,bits_A_phase,mtype)
        bits_B = merge(bits_B_rssi,bits_B_phase,mtype)
        
        ''' winnow信息协调 '''
        bits_A, bits_B = winnow(bits_A,bits_B,iteration[j])
        
        bmr[i,j] = BMR(bits_A,bits_B)
        bgr[i,j] = BGR(bits_A,sampling_time,sampling_period)

bmr = mean(bmr,0)
bgr = mean(bgr,0)

plt.figure(figsize=(8,5))
plt.plot(iteration,bmr,'bo-')
plt.xlabel('Iteration')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different iteration')

plt.figure(figsize=(8,5))
plt.plot(iteration,bgr,'bo-',)
plt.xlabel('Iteration')
plt.ylabel('Bit Generation Rate')
plt.title('BGR of different iteration')
