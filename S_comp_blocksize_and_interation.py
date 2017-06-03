# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 11:41:45 2016

@author: My402
"""

import os
import numpy as np
from numpy import zeros,size,mean
from function import BMR
from security_sampling import sampling
from security_quantize import quantization_thre,remain
from security_winnow   import winnow
from universal_statistical_test import Entropy
import matplotlib.pyplot as plt

os.system('cls')
plt.close('all')

sampling_period = 1     # 采样周期1ms
sampling_time = 3
SNR = 30
block_size = range(5,41,5)
coef = 0.8
iteration = [0,1,2,3,4]

group_num = 100
condi_num = size(block_size)
inter_num = size(iteration)
bmr = zeros((group_num,condi_num,inter_num))
bgr = zeros((group_num,condi_num,inter_num))
ent = zeros((group_num,condi_num,inter_num))

for i in range(group_num):
    for j in range(condi_num):
        for k in range(inter_num):
            print 'Running group:',i,j,k
            
            rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time,0.9,0.4)            
            bitsA,drop_listA = quantization_thre(rssi_A,block_size[j],coef)
            bitsB,drop_listB = quantization_thre(rssi_B,block_size[j],coef)
            bitsA = remain(bitsA,drop_listA,drop_listB)
            bitsB = remain(bitsB,drop_listA,drop_listB)
            bitsA,bitsB = winnow(bitsA,bitsB,iteration[k])
            
            bmr[i,j,k] = BMR(bitsA,bitsB)
            bgr[i,j,k] = size(bitsA)/(sampling_time*1000.0/sampling_period)
            #ent[i,j,k] = Entropy(bitsA)

bmr = mean(bmr,0)
bgr = mean(bgr,0)
ent = mean(ent,0)

''' block_size为横坐标'''
plt.figure(figsize=(8,5))
plt.plot(block_size,bmr[:,0],'ro-',label='No winnow')
plt.plot(block_size,bmr[:,1],'yo-',label='1 interation')
plt.plot(block_size,bmr[:,2],'go-',label='2 interations')
plt.plot(block_size,bmr[:,3],'bo-',label='3 interations')
plt.plot(block_size,bmr[:,4],'ko-',label='4 interations')
plt.xlabel('Block size')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different block sizes(coef=%.2f)'%coef)
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(block_size,bgr[:,0],'ro-',label='No winnow')
plt.plot(block_size,bgr[:,1],'yo-',label='1 interation')
plt.plot(block_size,bgr[:,2],'go-',label='2 interations')
plt.plot(block_size,bgr[:,3],'bo-',label='3 interations')
plt.plot(block_size,bgr[:,4],'ko-',label='4 interations')
plt.xlabel('Block size')
plt.ylabel('Bit Generate Rate')
plt.title('BGR of different block sizes(coef=%.2f)'%coef)
plt.legend()
plt.ylim(0,1)

plt.figure(figsize=(8,5))
plt.plot(block_size,ent[:,0],'ro-',label='No winnow')
plt.plot(block_size,ent[:,1],'yo-',label='1 interation')
plt.plot(block_size,ent[:,2],'go-',label='2 interations')
plt.plot(block_size,ent[:,3],'bo-',label='3 interations')
plt.plot(block_size,ent[:,4],'ko-',label='4 interations')
plt.xlabel('Block size')
plt.ylabel('Entropy')
plt.title('Entropy of different block sizes(coef=%.2f)'%coef)
plt.legend()

'''iteration为横坐标'''
plt.figure(figsize=(8,5))
plt.plot(iteration,bmr[0,:],'ro-',label='bl=%d'%(block_size[0]))
plt.plot(iteration,bmr[2,:],'yo-',label='bl=%d'%(block_size[2]))
plt.plot(iteration,bmr[4,:],'go-',label='bl=%d'%(block_size[4]))
plt.plot(iteration,bmr[6,:],'bo-',label='bl=%d'%(block_size[6]))
plt.xlabel('Iteration')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different iteration(coef=%.2f)'%(coef))
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(iteration,bgr[0,:],'ro-',label='bl=%d'%(block_size[0]))
plt.plot(iteration,bgr[2,:],'yo-',label='bl=%d'%(block_size[2]))
plt.plot(iteration,bgr[4,:],'go-',label='bl=%d'%(block_size[4]))
plt.plot(iteration,bgr[6,:],'bo-',label='bl=%d'%(block_size[6]))
plt.xlabel('Iteration')
plt.ylabel('Bit Generation Rate')
plt.title('BGR of different iteration(coef=%.2f)'%(coef))
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(iteration,ent[0,:],'ro-',label='bl=%d'%(block_size[0]))
plt.plot(iteration,ent[2,:],'yo-',label='bl=%d'%(block_size[2]))
plt.plot(iteration,ent[4,:],'go-',label='bl=%d'%(block_size[4]))
plt.plot(iteration,ent[6,:],'bo-',label='bl=%d'%(block_size[6]))
plt.xlabel('Iteration')
plt.ylabel('Entropy')
plt.title('Entropy of different iteration(coef=%.2f)'%(coef))
plt.legend()