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
from security_quantize import quantization_even

os.system('cls')
plt.close('all')

sampling_period = 1
sampling_time = 3
order = [1,2,3,4]
qtype = ['natural','gray']

group_num = 100
condi_num = size(order)
qtype_num = size(qtype)
bmr = zeros((group_num,condi_num,qtype_num))
bgr = zeros((group_num,condi_num,qtype_num))

for i in range(group_num):
    for j in range(condi_num):
        for k in range(qtype_num):
            print 'Running group:',i,j,k
        
            phase_A,phase_B,phase_E = mod(sampling('Phase',sampling_period,sampling_time,0.9,0.4), 2*pi)
            bitsA = quantization_even('Phase',phase_A,size(phase_A),qtype[k],order[j])
            bitsB = quantization_even('Phase',phase_B,size(phase_A),qtype[k],order[j])    
            
            bmr[i,j,k] = BMR(bitsA,bitsB)
            bgr[i,j,k] = BGR(bitsA,sampling_time,sampling_period)

bmr = mean(bmr,0)
bgr = mean(bgr,0)

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
