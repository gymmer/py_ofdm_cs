# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:06:28 2016

@author: My402
"""

import os
import numpy as np
from numpy import zeros,mean
import matplotlib.pyplot as plt
from pos_agreement_2 import agreement
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
gro_num = 100               # 进行多组取平均
mtype = ['RSSI', 'Phase', 'cross']

''' 比较不同的信噪比SNR '''
mtype_num = len(mtype)
SNR_num = len(SNR)
CS_MSE  = zeros((gro_num,SNR_num,mtype_num))
eva_MSE = zeros((gro_num,SNR_num,mtype_num))
CS_BER  = zeros((gro_num,SNR_num,mtype_num))
eva_BER = zeros((gro_num,SNR_num,mtype_num))
CS_SC   = zeros((gro_num,SNR_num,mtype_num))

for i in range(gro_num):
  for j in range(SNR_num):
      for k in range(mtype_num):
          print 'Running... Current group: ',i,j,k
          
          ''' 根据RSSI/Phase产生随机导频图样'''
          pos_A,pos_B,pos_E = agreement(P,mtype[k])
          
          ''' 发送端 '''
          bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
          
          ''' 信道传输 '''
          h_ab,H_ab,y_b = transmission(x,L,K,N,Ncp,SNR[j])
      
          ''' 接收端 信道估计'''
          h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,L,K,N,Ncp,pos_B,modulate_type,'CS','from_pos')
          
          ''' 窃听信道 '''
          h_ae,H_ae,y_e = transmission(x,L,K,N,Ncp,SNR[j])
          
          ''' 非法用户 '''
          h_eva, H_eva, bits_eva, diagram = receiver(y_e,L,K,N,Ncp,pos_E,modulate_type,'CS','from_pos')
          
          ''' 评价性能 '''
          CS_MSE[i,j,k]  = MSE(H_ab,H_cs)
          eva_MSE[i,j,k] = MSE(H_ae,H_eva)
          CS_BER[i,j,k]  = BMR(bits_A,bits_cs)
          eva_BER[i,j,k] = BMR(bits_A,bits_eva)
          CS_SC[i,j,k]   = SecCap(CS_BER[i,j,k],eva_BER[i,j,k])

''' 多组取平均 '''  
CS_MSE  = mean(CS_MSE,0)
eva_MSE = mean(eva_MSE,0)
CS_BER  = mean(CS_BER,0)
eva_BER = mean(eva_BER,0)
CS_SC   = mean(CS_SC,0)

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE[:,0], 'r.-',label='mtype:%s'%(mtype[0]))
plt.plot(SNR,CS_MSE[:,1], 'go-',label='mtype:%s'%(mtype[1]))
plt.plot(SNR,CS_MSE[:,2], 'bs-',label='mtype:%s'%(mtype[2]))
#plt.plot(SNR,CS_MSE[:,3], 'y*-',label='mtype:%s'%(mtype[3]))
#plt.plot(SNR,CS_MSE[:,4], 'c.-',label='mtype:%s'%(mtype[4]))
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,CS_BER[:,0], 'r.-',label='corr:%s'%(mtype[0]))
plt.semilogy(SNR,CS_BER[:,1], 'go-',label='corr:%s'%(mtype[1]))
plt.semilogy(SNR,CS_BER[:,2], 'bs-',label='corr:%s'%(mtype[2]))
#plt.semilogy(SNR,CS_BER[:,3], 'y*-',label='corr:%s'%(mtype[3]))
#plt.semilogy(SNR,CS_BER[:,4], 'c.-',label='corr:%s'%(mtype[4]))
plt.xlabel('weight')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_SC[:,0], 'r.-',label='corr:%s'%(mtype[0]))
plt.plot(SNR,CS_SC[:,1], 'go-',label='corr:%s'%(mtype[1]))
plt.plot(SNR,CS_SC[:,2], 'bs-',label='corr:%s'%(mtype[2]))
#plt.plot(SNR,CS_SC[:,3], 'y*-',label='corr:%s'%(mtype[3]))
#plt.plot(SNR,CS_SC[:,4], 'c.-',label='corr:%s'%(mtype[4]))
plt.xlabel('weight')
plt.ylabel('Capacity')
plt.title('Security Capacity')
plt.legend()

print 'Program Finished'