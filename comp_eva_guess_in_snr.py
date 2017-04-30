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
SNR = range(0,31,5)         # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
right = [2,10,20,30,35]     # 非法用户猜对导频数
gro_num = 10                # 进行多组取平均

''' 比较不同的信噪比SNR '''
SNR_num = len(SNR)
right_num = len(right)
CS_MSE  = zeros((gro_num,SNR_num,right_num))
eva_MSE = zeros((gro_num,SNR_num,right_num))
CS_BER  = zeros((gro_num,SNR_num,right_num))
eva_BER = zeros((gro_num,SNR_num,right_num))
SC      = zeros((gro_num,SNR_num,right_num))

for i in range(gro_num):
    for j in range(SNR_num):
        for r in range(right_num):
            print 'Running... Current group: ',i,j,r
            
            ''' 根据RSSI产生导频图样'''
            pos_A,pos_B,pos_E = agreement(2,2,P)
            
            ''' 发送端 '''
            bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
            
            ''' 信道传输 '''
            h,H,y = transmission(x,L,K,N,Ncp,SNR[j])
            
            ''' 接收端 信道估计'''
            h_cs,H_cs,bits_cs,diagram_cs = receiver(y,L,K,N,Ncp,pos_B,modulate_type,'CS','from_pos')
            
            ''' 非法用户 '''
            h_eva, H_eva, bits_eva, diagram = receiver(y,L,K,N,Ncp,pos_A,modulate_type,'CS','%d'%(right[r]))
            
            ''' 评价性能 '''
            CS_MSE[i,j,r]  = MSE(H,H_cs)
            eva_MSE[i,j,r] = MSE(H,H_eva)           
            CS_BER[i,j,r]  = BMR(bits_A,bits_cs)
            eva_BER[i,j,r] = BMR(bits_A,bits_eva)
            SC[i,j,r]      = SecCap(CS_BER[i,j,r],eva_BER[i,j,r])

''' 多组取平均 '''    
CS_MSE  = mean(CS_MSE,0)
eva_MSE = mean(eva_MSE,0)
CS_BER  = mean(CS_BER,0)
eva_BER = mean(eva_BER,0)
SC      = mean(SC,0)

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE[:,0], 'g*-.', label='Valid user')
plt.plot(SNR,eva_MSE[:,0],'r^--', label='EVA(guess %d right)'%(right[0]))
plt.plot(SNR,eva_MSE[:,1],'y<-.', label='EVA(guess %d right)'%(right[1]))
plt.plot(SNR,eva_MSE[:,2],'c>:',  label='EVA(guess %d right)'%(right[2]))
plt.plot(SNR,eva_MSE[:,3],'bv-.', label='EVA(guess %d right)'%(right[3]))
plt.plot(SNR,eva_MSE[:,4],'ms--', label='EVA(guess %d right)'%(right[4]))
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE of evasdropper by random guessing')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,CS_BER[:,0], 'g*-.', label='Valid user')
plt.semilogy(SNR,eva_BER[:,0],'r^--', label='EVA(guess %d right)'%(right[0]))
plt.semilogy(SNR,eva_BER[:,1],'y<-.', label='EVA(guess %d right)'%(right[1]))
plt.semilogy(SNR,eva_BER[:,2],'c>:',  label='EVA(guess %d right)'%(right[2]))
plt.semilogy(SNR,eva_BER[:,3],'bv-.', label='EVA(guess %d right)'%(right[3]))
plt.semilogy(SNR,eva_BER[:,4],'ms--', label='EVA(guess %d right)'%(right[4]))
plt.xlabel('SNR(dB)')
plt.ylabel('Probability')
plt.title('BER of evasdropper by random guessing')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(SNR,SC[:,0],'r^--',label='EVA(guess %d right)'%(right[0]))
plt.plot(SNR,SC[:,1],'y<-.',label='EVA(guess %d right)'%(right[1]))
plt.plot(SNR,SC[:,2],'c>:', label='EVA(guess %d right)'%(right[2]))
plt.plot(SNR,SC[:,3],'bv-.',label='EVA(guess %d right)'%(right[3]))
plt.plot(SNR,SC[:,4],'ms--',label='EVA(guess %d right)'%(right[4]))
plt.xlabel('SNR(dB)')
plt.ylabel('Capacity')
plt.title('Security Capacity of evasdropper by random guessing')
plt.legend()

print 'Program Finished'