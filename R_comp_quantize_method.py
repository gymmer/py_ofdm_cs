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
import matplotlib.pyplot as plt

os.system('cls')
plt.close('all')

sampling_period = 1     # 采样周期1ms
sampling_time = 20
block_size = 25

group_num = 5
condi_num = 9
bmr = zeros((group_num,condi_num))

for i in range(group_num):
    print 'Running group:',i
    
    rssi_A = sampling(sampling_period,sampling_time,1)
    rssi_B = sampling(sampling_period,sampling_time,1)+np.random.randint(1,5,size=(sampling_time/sampling_period*1000,1))

    bitsA = quantization_even(rssi_A,block_size,'gray',1)
    bitsB = quantization_even(rssi_B,block_size,'gray',1)
    bmr[i,0] = BMR(bitsA,bitsB)
    
    bitsA = quantization_even(rssi_A,block_size,'gray',2)
    bitsB = quantization_even(rssi_B,block_size,'gray',2)
    bmr[i,1] = BMR(bitsA,bitsB)
    
    bitsA = quantization_even(rssi_A,block_size,'gray',3)
    bitsB = quantization_even(rssi_B,block_size,'gray',3)
    bmr[i,2] = BMR(bitsA,bitsB)
    
    bitsA = quantization_even(rssi_A,block_size,'gray',4)
    bitsB = quantization_even(rssi_B,block_size,'gray',4)
    bmr[i,3] = BMR(bitsA,bitsB)
    
    bitsA = quantization_even(rssi_A,block_size,'natural',2)
    bitsB = quantization_even(rssi_B,block_size,'natural',2)
    bmr[i,4] = BMR(bitsA,bitsB)
    
    bitsA = quantization_even(rssi_A,block_size,'natural',3)
    bitsB = quantization_even(rssi_B,block_size,'natural',3)
    bmr[i,5] = BMR(bitsA,bitsB)
    
    bitsA = quantization_even(rssi_A,block_size,'natural',4)
    bitsB = quantization_even(rssi_B,block_size,'natural',4)
    bmr[i,6] = BMR(bitsA,bitsB)
    
    bitsA,drop_listA = quantization_thre(rssi_A,block_size,0)
    bitsB,drop_listB = quantization_thre(rssi_B,block_size,0)
    bmr[i,7] = BMR(bitsA,bitsB)
    
    coef = 0.2
    bitsA,drop_listA = quantization_thre(rssi_A,block_size,coef)
    bitsB,drop_listB = quantization_thre(rssi_B,block_size,coef)
    bitsA = remain(bitsA,drop_listA,drop_listB)
    bitsB = remain(bitsB,drop_listA,drop_listB)
    bmr[i,8] = BMR(bitsA,bitsB)
    
plt.figure(figsize=(8,5))
plt.plot(bmr[:,0],'ro-' ,label='even:1bit')
plt.plot(bmr[:,1],'y.-' ,label='even:2 Gray')
plt.plot(bmr[:,2],'g.-' ,label='even:3 Gray')
plt.plot(bmr[:,3],'c.-' ,label='even:4 Gray')
plt.plot(bmr[:,4],'ys--',label='even:2 Natural')
plt.plot(bmr[:,5],'gs--',label='even:3 Natural')
plt.plot(bmr[:,6],'cs--',label='even:4 Natural')
plt.plot(bmr[:,7],'b*-' ,label='threshold:coef=0')
plt.plot(bmr[:,8],'bp--',label='threshold:coef=0.2')
plt.legend()
plt.xlabel('Expriment')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different quantize methods(block_size=%d)'%(block_size))
