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
pos_ls = arange(0,N,5)      # LS估计的均匀导频图样
SNR = range(0,31,5)         # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM

''' 多组取平均 '''
gro_num = 100
SNR_num = len(SNR)
CS_MSE     = zeros((gro_num,SNR_num))
CS_BER     = zeros((gro_num,SNR_num))
CS_eva_MSE = zeros((gro_num,SNR_num))
CS_eva_BER = zeros((gro_num,SNR_num))
CS_SC      = zeros((gro_num,SNR_num))
LS_MSE     = zeros((gro_num,SNR_num))
LS_BER     = zeros((gro_num,SNR_num))
LS_eva_MSE = zeros((gro_num,SNR_num))
LS_eva_BER = zeros((gro_num,SNR_num))
LS_SC      = zeros((gro_num,SNR_num))

for i in range(gro_num):
    for j in range(SNR_num):
        print 'Running... Current group: ',i,j
        
        ''' CS '''
        pos_A,pos_B,pos_E = agreement(P)
        bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
        h_ab,H_ab,y_b = transmission(x,L,K,N,Ncp,SNR[j])
        h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,L,K,N,Ncp,pos_A,modulate_type,'CS','from_pos')
        h_ae,H_ae,y_e = transmission(x,L,K,N,Ncp,SNR[j])
        h_eva,H_eva,bits_eva,diagram = receiver(y_e,L,K,N,Ncp,pos_E,modulate_type,'CS','from_pos')
        CS_MSE[i,j]     = MSE(H_ab,H_cs)
        CS_eva_MSE[i,j] = MSE(H_ae,H_eva)
        CS_BER[i,j]     = BMR(bits_A,bits_cs)
        CS_eva_BER[i,j] = BMR(bits_A,bits_eva)
        CS_SC[i,j]      = SecCap(CS_BER[i,j],CS_eva_BER[i,j])
 
        ''' LS '''
        pos_A = pos_B = pos_E = pos_ls
        bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
        h_ab,H_ab,y_b = transmission(x,L,K,N,Ncp,SNR[j])
        h_ls,H_ls,bits_ls,diagram_ls = receiver(y_b,L,K,N,Ncp,pos_B,modulate_type,'LS','from_pos')
        h_ae,H_ae,y_e = transmission(x,L,K,N,Ncp,SNR[j])
        h_eva,H_eva,bits_eva,diagram = receiver(y_e,L,K,N,Ncp,pos_E,modulate_type,'LS','from_pos')
        LS_MSE[i,j]     = MSE(H_ab,H_ls)
        LS_eva_MSE[i,j] = MSE(H_ae,H_eva)
        LS_BER[i,j]     = BMR(bits_A,bits_ls)
        LS_eva_BER[i,j] = BMR(bits_A,bits_eva)
        LS_SC[i,j]      = SecCap(LS_BER[i,j],LS_eva_BER[i,j])
 
CS_MSE     = mean(CS_MSE,0)
CS_BER     = mean(CS_BER,0)
CS_eva_MSE = mean(CS_eva_MSE,0)
CS_eva_BER = mean(CS_eva_BER,0)
CS_SC      = mean(CS_SC,0)
LS_MSE     = mean(LS_MSE,0)
LS_BER     = mean(LS_BER,0)
LS_eva_MSE = mean(LS_eva_MSE,0)
LS_eva_BER = mean(LS_eva_BER,0)
LS_SC      = mean(LS_SC,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE,'g*-',label='CS(Random, P=%s)'%(P))
plt.plot(SNR,LS_MSE,'bo-',label='LS(Even, P=%s)'%(len(pos_ls)))
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,CS_BER,'g*-',label='CS(Random, P=%s)'%(P))
plt.semilogy(SNR,LS_BER,'bo-',label='LS(Even, P=%s)'%(len(pos_ls)))
plt.xlabel('SNR(dB)')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_SC,'g*-',label='CS(Random, P=%s)'%(P))
plt.plot(SNR,LS_SC,'bo-',label='LS(Even, P=%s)'%(len(pos_ls)))
plt.xlabel('SNR(dB)')
plt.ylabel('Capacity')
plt.title('Security Capacity')
plt.legend()

print 'Program Finished'