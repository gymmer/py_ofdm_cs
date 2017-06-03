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
P = 36                      # 导频数，P<N
SNR = range(0,31,5)         # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
gro_num = 100               # 进行多组取平均
weight = [0,0.3,0.6,0.9]

''' 比较不同的信噪比SNR '''
SNR_num = len(SNR)
wei_num = len(weight)
#lx_MSE  = zeros((gro_num,SNR_num,wei_num))
CS_MSE  = zeros((gro_num,SNR_num,wei_num))
eva_MSE = zeros((gro_num,SNR_num,wei_num))
#lx_BER  = zeros((gro_num,SNR_num,wei_num))
CS_BER  = zeros((gro_num,SNR_num,wei_num))
eva_BER = zeros((gro_num,SNR_num,wei_num))
#lx_SC   = zeros((gro_num,SNR_num,wei_num))
CS_SC   = zeros((gro_num,SNR_num,wei_num))

for i in range(gro_num):
    for j in range(SNR_num):
        for k in range(wei_num):
            print 'Running... Current group: ',i,j,k
            
            ''' 根据RSSI/Phase产生随机导频图样'''
            pos_A,pos_B,pos_E = agreement(P,weight[k])
            
            ''' 发送端 '''
            bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
            
            ''' 信道传输 '''
            h_ab,H_ab,y_b = transmission(x,L,K,N,Ncp,SNR[j])
            
            ''' 理想条件下的信道估计'''
            # 合法用户确切知道发送端导频
            #h_lx,H_lx,bits_lx,diagram_lx = receiver(y_b,L,K,N,Ncp,pos_A,modulate_type,'CS','from_pos')
        
            ''' 接收端 信道估计'''
            h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,L,K,N,Ncp,pos_B,modulate_type,'CS','from_pos')
            
            ''' 窃听信道 '''
            h_ae,H_ae,y_e = transmission(x,L,K,N,Ncp,SNR[j])
            
            ''' 非法用户 '''
            h_eva, H_eva, bits_eva, diagram = receiver(y_e,L,K,N,Ncp,pos_E,modulate_type,'CS','from_pos')
            
            ''' 评价性能 '''
            #lx_MSE[i,j,k]  = MSE(H_ab,H_lx)
            CS_MSE[i,j,k]  = MSE(H_ab,H_cs)
            eva_MSE[i,j,k] = MSE(H_ae,H_eva)   
            #lx_BER[i,j,k]  = BMR(bits_A,bits_lx)
            CS_BER[i,j,k]  = BMR(bits_A,bits_cs)
            eva_BER[i,j,k] = BMR(bits_A,bits_eva)
            #lx_SC[i,j,k]   = SecCap(lx_BER[i,j],eva_BER[i,j])
            CS_SC[i,j,k]   = SecCap(CS_BER[i,j,k],eva_BER[i,j,k])

''' 多组取平均 ''' 
#lx_MSE  = mean(lx_MSE,0)   
CS_MSE  = mean(CS_MSE,0)
eva_MSE = mean(eva_MSE,0)
#lx_BER  = mean(lx_BER,0)
CS_BER  = mean(CS_BER,0)
eva_BER = mean(eva_BER,0)
#lx_SC   = mean(lx_SC,0)
CS_SC   = mean(CS_SC,0)

plt.figure(figsize=(8,5))
#plt.plot(SNR,lx_MSE, 'bo-',label='Ideal user')
plt.plot(SNR,CS_MSE[:,0], 'y*-',label='Valid user-0')
plt.plot(SNR,CS_MSE[:,1], 'g*-',label='Valid user-0.3')
plt.plot(SNR,CS_MSE[:,2], 'c*-',label='Valid user-0.6')
plt.plot(SNR,CS_MSE[:,3], 'b*-',label='Valid user-0.9')
#plt.plot(SNR,eva_MSE,'r^--',label='Evasdropper')
plt.xlabel('SNR')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
#plt.semilogy(SNR,lx_BER, 'bo-',label='Ideal user')
plt.semilogy(SNR,CS_BER[:,0], 'y*-',label='Valid user-0')
plt.semilogy(SNR,CS_BER[:,1], 'g*-',label='Valid user-0.3')
plt.semilogy(SNR,CS_BER[:,2], 'c*-',label='Valid user-0.6')
plt.semilogy(SNR,CS_BER[:,3], 'b*-',label='Valid user-0.9')
#plt.semilogy(SNR,eva_BER,'r^--',label='Evasdropper')
plt.xlabel('SNR')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

plt.figure(figsize=(8,5))
#plt.plot(SNR,lx_SC,'bo-',label='Ideal user')
plt.plot(SNR,CS_SC[:,0], 'y*-',label='Valid user-0')
plt.plot(SNR,CS_SC[:,1], 'g*-',label='Valid user-0.3')
plt.plot(SNR,CS_SC[:,2], 'c*-',label='Valid user-0.6')
plt.plot(SNR,CS_SC[:,3], 'b*-',label='Valid user-0.9')
plt.xlabel('SNR')
plt.ylabel('Capacity')
plt.title('Security Capacity')
plt.legend()

print 'Program Finished'