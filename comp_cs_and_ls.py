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
from function import MSE,BMR
  
os.system('cls')
plt.close('all')

L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
Ncp = 60                    # 循环前缀的长度,Ncp>L
P = [36,103]                # 导频数，P<N 
SNR = range(0,31,5)         # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
gro_num = 10                # 进行多组取平均

''' 比较不同的信噪比SNR '''
SNR_num = len(SNR)
CS_MSE  = zeros((gro_num,SNR_num))
LS_MSE  = zeros((gro_num,SNR_num))
eva_MSE = zeros((gro_num,SNR_num))
CS_BER  = zeros((gro_num,SNR_num))
LS_BER  = zeros((gro_num,SNR_num))
eva_BER = zeros((gro_num,SNR_num))

for i in range(gro_num):
    for j in range(SNR_num):
        print 'Running... Current group: ',i,j
        
        ''' 根据RSSI产生导频图样'''
        pos_A,pos_B,pos_E = agreement(2,2,P[0])
        
        ''' 发送端 '''
        bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)

        ''' 信道传输 '''
        h,H,y = transmission(x,L,K,N,Ncp,SNR[j])
        
        ''' 接收端 信道估计'''
        h_cs,H_cs,bits_cs,diagram_cs = receiver(y,L,K,N,Ncp,pos_B,modulate_type,'CS','from_pos')
        h_ls,H_ls,bits_ls,diagram_ls = receiver(y,L,K,N,Ncp,pos_B,modulate_type,'LS','from_pos')
        
        ''' 非法用户 '''
        h_eva,H_eva,bits_eva,diagram_eva = receiver(y,L,K,N,Ncp,pos_E,modulate_type,'CS','from_pos')
        
        ''' 评价性能：MSE '''
        CS_MSE[i,j]  = MSE(H,H_cs)
        LS_MSE[i,j]  = MSE(H,H_ls)
        eva_MSE[i,j] = MSE(H,H_eva)
        CS_BER[i,j]  = BMR(bits_A,bits_cs)
        LS_BER[i,j]  = BMR(bits_A,bits_ls)
        eva_BER[i,j] = BMR(bits_A,bits_eva)
          
CS_MSE_0  = mean(CS_MSE,0)
LS_MSE_0  = mean(LS_MSE,0)
eva_MSE_0 = mean(eva_MSE,0)
CS_BER_0  = mean(CS_BER,0)
LS_BER_0  = mean(LS_BER,0)
eva_BER_0 = mean(eva_BER,0)

for i in range(gro_num):
    for j in range(SNR_num):
        print 'Running... Current group: ',i,j
        
        ''' 均匀的导频图样 '''
        # 导频插入的位置。每5个插入一个导频。取值{0，5，10，...，510}，共P=103个
        pos = arange(P[1])*5
        
        ''' 发送端 '''
        bits_A,diagram_A,x = sender(N,Ncp,pos,modulate_type)
        
        ''' 信道传输 ''' 
        h,H,y = transmission(x,L,K,N,Ncp,SNR[j])
        
        ''' 接收端 信道估计''' 
        h_ls,H_ls,bits_ls,diagram_ls = receiver(y,L,K,N,Ncp,pos,modulate_type,'LS','from_pos')
        
        ''' 评价性能 '''
        LS_MSE[i,j]  = MSE(H,H_ls)
        LS_BER[i,j]  = BMR(bits_A,bits_ls)

''' 多组取平均 '''
LS_MSE_1 = mean(LS_MSE,0)
LS_BER_1  = mean(LS_BER,0)

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE_0, 'go-' ,label='CS,P=%d,RSSI'%(P[0]))
plt.plot(SNR,LS_MSE_0, 'bo-' ,label='LS,P=%d,RSSI'%(P[0]))
plt.plot(SNR,eva_MSE_0,'rp-' ,label='eva,P=%d,RSSI'%(P[0]))
plt.plot(SNR,LS_MSE_1, 'b+-.',label='LS,P=%d,even'%(P[1]))
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE of CS/LS')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,CS_BER_0, 'go-' ,label='CS,P=%d,RSSI'%(P[0]))
plt.semilogy(SNR,LS_BER_0, 'bo-' ,label='LS,P=%d,RSSI'%(P[0]))
plt.semilogy(SNR,eva_BER_0,'rp-' ,label='eva,P=%d,RSSI'%(P[0]))
plt.semilogy(SNR,LS_BER_1, 'b+-.',label='LS,P=%d,even'%(P[1]))
plt.xlabel('SNR(dB)')
plt.ylabel('Probability')
plt.title('BER of CS/LS')
plt.legend()

print 'Program Finished'