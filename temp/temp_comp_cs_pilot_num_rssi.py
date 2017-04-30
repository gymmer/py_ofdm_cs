# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:06:28 2016

@author: My402
"""

import os
from numpy import zeros,mean
import matplotlib.pyplot as plt
from pos_agreement import agreement
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
P = [4*K,6*K,8*K,10*K,15*K] # 导频数，P<N
SNR = range(0,31,5)         # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
gro_num = 10                # 进行多组取平均

''' 比较不同的信噪比SNR '''
P_num   = len(P)
SNR_num = len(SNR)
CS_MSE  = zeros((gro_num,SNR_num,P_num))
CS_BER  = zeros((gro_num,SNR_num,P_num))
CS_SC   = zeros((gro_num,SNR_num,P_num))

for i in range(gro_num):
    for j in range(SNR_num):
        for p in range(P_num):
            print 'Running... Current group: ',i,j,p
            
            ''' 根据RSSI/Phase产生随机导频图样'''
            pos_A,pos_B,pos_E = agreement(2,P[p],0.5)
            
            ''' 发送端 '''
            bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
    
            ''' 信道传输 '''
            h,H,y = transmission(x,L,K,N,Ncp,SNR[j])
            
            ''' 接收端 信道估计'''
            h_cs,H_cs,bits_cs,diagram_cs = receiver(y,L,K,N,Ncp,pos_B,modulate_type,'CS','from_pos')
            h_eva,H_eva,bits_eva,diagram_eva = receiver(y,L,K,N,Ncp,pos_E,modulate_type,'CS','from_pos')
            
            ''' 评价性能 '''
            CS_MSE[i,j,p] = MSE(H,H_cs)
            CS_BER[i,j,p] = BMR(bits_A,bits_cs)
            CS_SC[i,j,p]  = SecCap(BMR(bits_A,bits_cs), BMR(bits_A,bits_eva))
          
CS_MSE = mean(CS_MSE,0)
CS_BER = mean(CS_BER,0)
CS_SC  = mean(CS_SC,0)

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE[:,0], 'ro-' ,label='P=%d'%(P[0]))
plt.plot(SNR,CS_MSE[:,1], 'y*-' ,label='P=%d'%(P[1]))
plt.plot(SNR,CS_MSE[:,2], 'g+-' ,label='P=%d'%(P[2]))
plt.plot(SNR,CS_MSE[:,3], 'bs-' ,label='P=%d'%(P[3]))
plt.plot(SNR,CS_MSE[:,4], 'mx-' ,label='P=%d'%(P[4]))
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE of CS & Random Pilot')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,CS_BER[:,0], 'ro-' ,label='P=%d'%(P[0]))
plt.semilogy(SNR,CS_BER[:,1], 'y*-' ,label='P=%d'%(P[1]))
plt.semilogy(SNR,CS_BER[:,2], 'g+-' ,label='P=%d'%(P[2]))
plt.semilogy(SNR,CS_BER[:,3], 'bs-' ,label='P=%d'%(P[3]))
plt.semilogy(SNR,CS_BER[:,4], 'mx-' ,label='P=%d'%(P[4]))
plt.xlabel('SNR(dB)')
plt.ylabel('BER')
plt.title('BER of CS & Random Pilot')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_SC[:,0], 'ro-' ,label='P=%d'%(P[0]))
plt.plot(SNR,CS_SC[:,1], 'y*-' ,label='P=%d'%(P[1]))
plt.plot(SNR,CS_SC[:,2], 'g+-' ,label='P=%d'%(P[2]))
plt.plot(SNR,CS_SC[:,3], 'bs-' ,label='P=%d'%(P[3]))
plt.plot(SNR,CS_SC[:,4], 'mx-' ,label='P=%d'%(P[4]))
plt.xlabel('SNR(dB)')
plt.ylabel('Capacity')
plt.title('Security Capacity of CS & Random Pilot')
plt.legend()

print 'Program Finished'