# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean,arange

sys.path.append('../')
from util.metric import MSE,BMR,SecCap
from KG import agreement
from OFDM import sender,transmission,receiver
  
os.system('cls')
plt.close('all')

''' 信道参数 '''
L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
Ncp = 60                    # 循环前缀的长度,Ncp>L
P = 36                      # CS估计导频数，P<N
pos_even = arange(1,N,15)   # 均匀导频图样
SNR = range(0,31,5)         # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM

''' 多组取平均 '''
gro_num        = 100
SNR_num        = len(SNR)
random_MSE     = zeros((gro_num,SNR_num))
random_BER     = zeros((gro_num,SNR_num))
random_eva_MSE = zeros((gro_num,SNR_num))
random_eva_BER = zeros((gro_num,SNR_num))
random_SC      = zeros((gro_num,SNR_num))
even_MSE       = zeros((gro_num,SNR_num))
even_BER       = zeros((gro_num,SNR_num))
even_eva_MSE   = zeros((gro_num,SNR_num))
even_eva_BER   = zeros((gro_num,SNR_num))
even_SC        = zeros((gro_num,SNR_num))

for i in range(gro_num):
    for j in range(SNR_num):
        print 'Running... Current group: ',i,j
        
        ''' Random pilot '''
        pos_A,pos_B,pos_E = agreement(P)
        bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
        h_ab,H_ab,y_b = transmission(x,L,K,N,Ncp,SNR[j])
        h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,L,K,N,Ncp,pos_A,modulate_type)
        h_ae,H_ae,y_e = transmission(x,L,K,N,Ncp,SNR[j])
        h_eva,H_eva,bits_eva,diagram = receiver(y_e,L,K,N,Ncp,pos_E,modulate_type)
        random_MSE[i,j]     = MSE(H_ab,H_cs)
        random_eva_MSE[i,j] = MSE(H_ab,H_eva)
        random_BER[i,j]     = BMR(bits_A,bits_cs)
        random_eva_BER[i,j] = BMR(bits_A,bits_eva)
        random_SC[i,j]      = SecCap(random_BER[i,j],random_eva_BER[i,j])
 
        ''' Even pilot '''
        pos_A = pos_B = pos_E = pos_even
        bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
        h_ab,H_ab,y_b = transmission(x,L,K,N,Ncp,SNR[j])
        h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,L,K,N,Ncp,pos_A,modulate_type)
        h_ae,H_ae,y_e = transmission(x,L,K,N,Ncp,SNR[j])
        h_eva,H_eva,bits_eva,diagram = receiver(y_e,L,K,N,Ncp,pos_E,modulate_type)
        even_MSE[i,j]     = MSE(H_ab,H_cs)
        even_eva_MSE[i,j] = MSE(H_ab,H_eva)
        even_BER[i,j]     = BMR(bits_A,bits_cs)
        even_eva_BER[i,j] = BMR(bits_A,bits_eva)
        even_SC[i,j]      = SecCap(even_BER[i,j],even_eva_BER[i,j])

random_MSE     = mean(random_MSE,0)
random_BER     = mean(random_BER,0)
random_eva_MSE = mean(random_eva_MSE,0)
random_eva_BER = mean(random_eva_BER,0)
random_SC      = mean(random_SC,0)
even_MSE       = mean(even_MSE,0)
even_BER       = mean(even_BER,0)
even_eva_MSE   = mean(even_eva_MSE,0)
even_eva_BER   = mean(even_eva_BER,0)
even_SC        = mean(even_SC,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(SNR,random_MSE,'ko-',label='Random')
plt.plot(SNR,even_MSE,  'k^:',label='Even')
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,random_BER,'ko-',label='Random')
plt.semilogy(SNR,even_BER,  'k^:',label='Even')
plt.xlabel('SNR(dB)')
plt.ylabel('BER')
plt.title('BER')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.plot(SNR,random_SC,'ko-',label='Random')
plt.plot(SNR,even_SC,  'k^:',label='Even')
plt.xlabel('SNR(dB)')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.legend()
plt.show()

print 'Program Finished'