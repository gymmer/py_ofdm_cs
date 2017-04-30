# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:06:28 2016

@author: My402
"""

import os
from numpy import zeros,mean,arange
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
SNR = range(0,31,5)         # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
gro_num = 10                # 进行多组取平均

''' 比较不同的信噪比SNR '''
SNR_num = len(SNR)
CS_MSE  = zeros((gro_num,SNR_num))
CS_Pe   = zeros((gro_num,SNR_num))
CS_SC   = zeros((gro_num,SNR_num))

for i in range(gro_num):
    for j in range(SNR_num):
        print 'Running... Current group: ',i,j
        
        ''' 根据RSSI产生导频图样'''
        pos_A,pos_B,pos_E = agreement(2,2,P)
        
        ''' 发送端 '''
        bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)

        ''' 信道传输 '''
        h,H,W,y = transmission(x,L,K,N,Ncp,SNR[j])
        
        ''' 接收端 信道估计'''
        h_cs,H_cs,bits_cs,diagram_cs = receiver(y,L,K,N,Ncp,pos_B,modulate_type,'CS','from_pos')
        
        ''' 非法用户 '''
        h_eva,H_eva,bits_eva,diagram_eva = receiver(y,L,K,N,Ncp,pos_E,modulate_type,'CS','from_pos')
        
        ''' 评价性能：MSE '''
        CS_MSE[i,j] = MSE(H,H_cs)       
        CS_Pe[i,j]  = BMR(bits_A,bits_cs)
        CS_SC[i,j]  = SecCap(BMR(bits_A,bits_cs), BMR(bits_A,bits_eva)) 
          
CS_MSE_0 = mean(CS_MSE,0)
CS_Pe_0  = mean(CS_Pe,0)
CS_SC_0  = mean(CS_SC,0)

for i in range(gro_num):
    for j in range(SNR_num):
        print 'Running... Current group: ',i,j
        
        ''' 均匀的导频图样 '''
        # 导频插入的位置。每14个插入一个导频。
        pos = arange(P)*14
        
        ''' 发送端 '''
        bits_A,diagram_A,x = sender(N,Ncp,pos,modulate_type)
        
        ''' 信道传输 ''' 
        h,H,W,y = transmission(x,L,K,N,Ncp,SNR[j])
        
        ''' 接收端 信道估计''' 
        h_cs,H_ls,bits_cs,diagram_cs = receiver(y,L,K,N,Ncp,pos,modulate_type,'CS','from_pos')
        
        ''' 评价性能 '''
        CS_MSE[i,j]  = MSE(H,H_ls)
        CS_Pe[i,j]  = BMR(bits_A,bits_cs)
        CS_SC[i,j]  = SecCap(BMR(bits_A,bits_cs), BMR(bits_A,bits_eva)) 

''' 多组取平均 '''
CS_MSE_1 = mean(CS_MSE,0)
CS_Pe_1  = mean(CS_Pe,0)
CS_SC_1  = mean(CS_SC,0)

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE_0, 'go-' ,label='RSSI')
plt.plot(SNR,CS_MSE_1, 'b+-.',label='Even')
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE of CS & P=%d'%(P))
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,CS_Pe_0, 'go-' ,label='RSSI')
plt.semilogy(SNR,CS_Pe_1, 'b+-.',label='Even')
plt.xlabel('SNR(dB)')
plt.ylabel('Probability')
plt.title('Pe of CS & P=%d'%(P))
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,CS_SC_0, 'go-' ,label='RSSI')
plt.semilogy(SNR,CS_SC_1, 'b+-.',label='Even')
plt.xlabel('SNR(dB)')
plt.ylabel('Capacity')
plt.title('Security Capacity of CS & P=%d'%(P))
plt.legend()

print 'Program Finished'