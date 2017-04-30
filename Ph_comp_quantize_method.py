# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:41:45 2016

@author: My402
"""

import os
import numpy as np
from numpy import zeros,size,mean,mod,pi
from function import BMR
from universal_statistical_test import Entropy
from Phase_sampling import sampling
from Phase_quantization import quantization_even
from part_transmission import awgn
import matplotlib.pyplot as plt

os.system('cls')
plt.close('all')

sampling_period = 1     # 采样周期1ms
sampling_time = 20
N = sampling_time/sampling_period*1000
SNR = 30
order = [1,2,3,4]
qtype = ['natural','gray']

group_num = 5
condi_num = size(order)
qtype_num = size(qtype)
bmr = zeros((group_num,condi_num,qtype_num))
bgr = zeros((group_num,condi_num,qtype_num))
ent = zeros((group_num,condi_num,qtype_num))

for i in range(group_num):
    for j in range(condi_num):
        for k in range(qtype_num):
            print 'Running group:',i,j,k
        
            phase_A = sampling(N)
            phase_B = mod(awgn(phase_A,SNR),2*pi)
        
            bitsA = quantization_even(phase_A,qtype[k],order[j])
            bitsB = quantization_even(phase_B,qtype[k],order[j])        
            bmr[i,j,k] = BMR(bitsA,bitsB)
            bgr[i,j,k] = size(bitsA)/(sampling_time/sampling_period*1000.0)
            ent[i,j,k] = Entropy(bitsA)

bmr = mean(bmr,0)
bgr = mean(bgr,0)
ent = mean(ent,0)

plt.figure(figsize=(8,5))
plt.plot(order,bmr[:,0],'bo-',label=qtype[0])
plt.plot(order,bmr[:,1],'go-',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different order')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(order,bgr[:,0],'bo-',label=qtype[0])
plt.plot(order,bgr[:,1],'go-',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('Bit Generate Rate')
plt.title('BGR of different order')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(order,ent[:,0],'bo-',label=qtype[0])
plt.plot(order,ent[:,1],'go-',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('Entropy')
plt.title('Entropy of different order')
plt.legend()