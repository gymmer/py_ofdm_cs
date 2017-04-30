# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:06:28 2016

@author: My402
"""

import os
from numpy import zeros,mean
import matplotlib.pyplot as plt
from RSSI_pos_agreement import agreement
from part_sender import sender
from part_transmission import transmission
from part_receiver import receiver
from function import MSE,BMR,SecCap
  
os.system('cls')
plt.close('all')

L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
Ncp = 60                    # 循环前缀的长度,Ncp>L
P = 36                      # 导频数，P<N
SNR = 30                    # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
right = range(P+1)          # 非法用户猜对导频数
gro_num = 10                # 进行多组取平均

right_num = len(right)
CS_MSE  = zeros((gro_num,right_num))
eva_MSE = zeros((gro_num,right_num))
CS_Pe   = zeros((gro_num,right_num))
eva_Pe  = zeros((gro_num,right_num))
SC      = zeros((gro_num,right_num))

for i in range(gro_num):
    for j in range(right_num):
        print 'Running... Current group: ',i,j
        
        ''' 根据RSSI产生导频图样'''
        pos_A,pos_B,pos_E = agreement(2,2,P)
        
        ''' 发送端 '''
        bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
        
        ''' 信道传输 '''
        h,H,W,y = transmission(x,L,K,N,Ncp,SNR)
        
        ''' 接收端 信道估计'''
        h_cs,H_cs,bits_cs,diagram_cs = receiver(y,L,K,N,Ncp,pos_B,modulate_type,'CS','from_pos')
        
        ''' 非法用户 '''
        # 非法用户随机猜测导频位置。与发送端的导频图样pos_A相比，非法用户猜对了j个,j取值[0,P)
        h_eva,H_eva,bits_eva,diagram_eva = receiver(y,L,K,N,Ncp,pos_A,modulate_type,'CS','%d'%(j))
        
        ''' 评价性能 '''
        CS_MSE[i,j]  = MSE(H,H_cs)
        eva_MSE[i,j] = MSE(H,H_eva)
        CS_Pe[i,j]   = BMR(bits_A,bits_cs)
        eva_Pe[i,j]  = BMR(bits_A,bits_eva)
        SC[i,j]      = SecCap(CS_Pe[i,j],eva_Pe[i,j])

''' 多组取平均 '''
CS_MSE  = mean(CS_MSE,0)
eva_MSE = mean(eva_MSE,0)
CS_Pe   = mean(CS_Pe,0)
eva_Pe  = mean(eva_Pe,0)
SC      = mean(SC,0)

plt.figure(figsize=(8,5))
plt.plot(right,CS_MSE, 'go-',label='Valid user')
plt.plot(right,eva_MSE,'ro-',label='Eevasdropper')
plt.xlabel('number of right pilots')
plt.ylabel('MSE(dB)')
plt.title('MSE of evasdropper by random guessing(SNR=%d)'%(SNR))
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(right,CS_Pe, 'go-',label='Valid user')
plt.semilogy(right,eva_Pe,'ro-',label='Eevasdropper')
plt.xlabel('number of right pilots')
plt.ylabel('Probability')
plt.title('Pe of evasdropper by random guessing(SNR=%d)'%(SNR))
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(right,SC, 'bo-')
plt.xlabel('number of right pilots')
plt.ylabel('Capacity')
plt.title('Security Capacity by random guessing(SNR=%d)'%(SNR))

print 'Program Finished'