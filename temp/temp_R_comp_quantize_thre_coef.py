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
coef = [i/10.0 for i in range(10)]
interation = [0,1,2,3,4]

group_num = 1
condi_num = size(coef)
inter_num = size(interation)
bmr = zeros((group_num,condi_num,inter_num))
bgr = zeros((group_num,condi_num,inter_num))
ent = zeros((group_num,condi_num,inter_num))

for i in range(group_num):
    for j in range(condi_num):
        for k in range(inter_num):
            print 'Running group:',i,j,k
        
            rssi_A = sampling(sampling_period,sampling_time,3)
            rssi_B = awgn(rssi_A,SNR)
        
            bitsA,drop_listA = quantization_thre(rssi_A,block_size,coef[j])
            bitsB,drop_listB = quantization_thre(rssi_B,block_size,coef[j])
            bitsA = remain(bitsA,drop_listA,drop_listB)
            bitsB = remain(bitsB,drop_listA,drop_listB)
            bitsA,bitsB = winnow(bitsA,bitsB,interation[k])
                       
            bmr[i,j,k] = BMR(bitsA,bitsB)
            bgr[i,j,k] = size(bitsA)/(sampling_time/sampling_period*1000.0)
            ent[i,j,k] = Entropy(bitsA)

bmr = mean(bmr,0)
bgr = mean(bgr,0)
ent = mean(ent,0)

plt.figure(figsize=(8,5))
plt.plot(coef,bmr[:,0],'ro-',label='No winnow')
plt.plot(coef,bmr[:,1],'yo-',label='1 interation')
plt.plot(coef,bmr[:,2],'go-',label='2 interations')
plt.plot(coef,bmr[:,3],'bo-',label='3 interations')
plt.plot(coef,bmr[:,4],'ko-',label='4 interations')
plt.xlabel('Coefficient')
plt.ylabel('Bit Mismatch Rate')
plt.title('BMR of different coef in thresold method(bl=%d)'%(block_size))
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(coef,bgr[:,0],'ro-',label='No winnow')
plt.plot(coef,bgr[:,1],'yo-',label='1 interation')
plt.plot(coef,bgr[:,2],'go-',label='2 interations')
plt.plot(coef,bgr[:,3],'bo-',label='3 interations')
plt.plot(coef,bgr[:,4],'ko-',label='4 interations')
plt.xlabel('Coefficient')
plt.ylabel('Bit Generate Rate')
plt.title('BGR of different coef in thresold method(bl=%d)'%(block_size))
plt.legend()
plt.ylim(0,1)

plt.figure(figsize=(8,5))
plt.plot(coef,ent[:,0],'ro-',label='No winnow')
plt.plot(coef,ent[:,1],'yo-',label='1 interation')
plt.plot(coef,ent[:,2],'go-',label='2 interations')
plt.plot(coef,ent[:,3],'bo-',label='3 interations')
plt.plot(coef,ent[:,4],'ko-',label='4 interations')
plt.xlabel('Coefficient')
plt.ylabel('Entropy')
plt.title('Entropy of different coef in thresold method(bl=%d)'%(block_size))
plt.legend()
plt.ylim(0,1)
