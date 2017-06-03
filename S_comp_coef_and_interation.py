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
block_size = 25
coef = [i/10.0 for i in range(10)]
iteration = [0,1,2,3,4]

group_num = 100
condi_num = size(coef)
inter_num = size(iteration)
bmr = zeros((group_num,condi_num,inter_num))
bgr = zeros((group_num,condi_num,inter_num))
ent = zeros((group_num,condi_num,inter_num))

for i in range(group_num):
    for j in range(condi_num):
        for k in range(inter_num):
            print 'Running group:',i,j,k
        
            rssi_A,rssi_B,rssi_E = sampling('RSSI',sampling_period,sampling_time,0.9,0.4)        
            bitsA,drop_listA = quantization_thre(rssi_A,block_size,coef[j])
            bitsB,drop_listB = quantization_thre(rssi_B,block_size,coef[j])
            bitsA = remain(bitsA,drop_listA,drop_listB)
            bitsB = remain(bitsB,drop_listA,drop_listB)
            bitsA,bitsB = winnow(bitsA,bitsB,iteration[k])
                       
            bmr[i,j,k] = BMR(bitsA,bitsB)
            bgr[i,j,k] = size(bitsA)/(sampling_time*1000.0/sampling_period)
            #ent[i,j,k] = Entropy(bitsA)

bmr = mean(bmr,0)
bgr = mean(bgr,0)
ent = mean(ent,0)

''' coef 为横坐标 '''
plt.figure(figsize=(8,5))
plt.plot(coef,bmr[:,0],'ro-',label='No winnow')
plt.plot(coef,bmr[:,1],'yo-',label='1 iteration')
plt.plot(coef,bmr[:,2],'go-',label='2 iterations')
plt.plot(coef,bmr[:,3],'bo-',label='3 iterations')
plt.plot(coef,bmr[:,4],'ko-',label='4 iterations')
plt.xlabel('Coefficient')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different coef(bl=%d)'%(block_size))
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(coef,bgr[:,0],'ro-',label='No winnow')
plt.plot(coef,bgr[:,1],'yo-',label='1 iteration')
plt.plot(coef,bgr[:,2],'go-',label='2 iterations')
plt.plot(coef,bgr[:,3],'bo-',label='3 iterations')
plt.plot(coef,bgr[:,4],'ko-',label='4 iterations')
plt.xlabel('Coefficient')
plt.ylabel('Bit Generate Rate')
plt.title('BGR of different coef(bl=%d)'%(block_size))
plt.legend()
plt.ylim(0,1)

plt.figure(figsize=(8,5))
plt.plot(coef,ent[:,0],'ro-',label='No winnow')
plt.plot(coef,ent[:,1],'yo-',label='1 iteration')
plt.plot(coef,ent[:,2],'go-',label='2 iterations')
plt.plot(coef,ent[:,3],'bo-',label='3 iterations')
plt.plot(coef,ent[:,4],'ko-',label='4 iterations')
plt.xlabel('Coefficient')
plt.ylabel('Entropy')
plt.title('Entropy of different coef(bl=%d)'%(block_size))
plt.legend()
plt.ylim(0,1)

''' iteration为横坐标 '''
plt.figure(figsize=(8,5))
plt.plot(iteration,bmr[2,:],'ro-',label='coef=0.2')
plt.plot(iteration,bmr[4,:],'yo-',label='coef=0.4')
plt.plot(iteration,bmr[6,:],'go-',label='coef=0.6')
plt.plot(iteration,bmr[8,:],'bo-',label='coef=0.8')
plt.xlabel('Iteration')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different iteration(bl=%d)'%(block_size))
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(iteration,bgr[2,:],'ro-',label='coef=0.2')
plt.plot(iteration,bgr[4,:],'yo-',label='coef=0.4')
plt.plot(iteration,bgr[6,:],'go-',label='coef=0.6')
plt.plot(iteration,bgr[8,:],'bo-',label='coef=0.8')
plt.xlabel('Iteration')
plt.ylabel('Bit Generate Rate')
plt.title('BGR of different iteration(bl=%d)'%(block_size))
plt.legend()
plt.ylim(0,1)

plt.figure(figsize=(8,5))
plt.plot(iteration,ent[2,:],'ro-',label='coef=0.2')
plt.plot(iteration,ent[4,:],'yo-',label='coef=0.4')
plt.plot(iteration,ent[6,:],'go-',label='coef=0.6')
plt.plot(iteration,ent[8,:],'bo-',label='coef=0.8')
plt.xlabel('Iteration')
plt.ylabel('Entropy')
plt.title('Entropy of different iteration(bl=%d)'%(block_size))
plt.legend()
plt.ylim(0,1)
