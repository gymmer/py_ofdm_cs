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
P = arange(4,60,4)          # 导频数，P<N
SNR = 20                    # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM

''' 多组取平均 '''
gro_num = 100
P_num = len(P)
bob_MSE = zeros((gro_num,P_num))
eva_MSE = zeros((gro_num,P_num))
bob_BER = zeros((gro_num,P_num))
eva_BER = zeros((gro_num,P_num))
SC      = zeros((gro_num,P_num))

for i in range(gro_num):
    for j in range(P_num):
        print 'Running... Current group: ',i,j
        
        pos_A,pos_B,pos_E = agreement(P[j])
        bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
        h_ab,H_ab,y_b = transmission(x,L,K,N,Ncp,SNR)
        h_lx,H_lx,bits_lx,diagram_lx = receiver(y_b,L,K,N,Ncp,pos_A,modulate_type)
        h_ae,H_ae,y_e = transmission(x,L,K,N,Ncp,SNR)
        h_eva,H_eva,bits_eva,diagram = receiver(y_e,L,K,N,Ncp,pos_E,modulate_type)
        bob_MSE[i,j] = MSE(H_ab,H_lx)
        eva_MSE[i,j] = MSE(H_ae,H_eva)   
        bob_BER[i,j] = BMR(bits_A,bits_lx)
        eva_BER[i,j] = BMR(bits_A,bits_eva)
        SC[i,j]      = SecCap(bob_BER[i,j],eva_BER[i,j])

bob_MSE = mean(bob_MSE,0)   
eva_MSE = mean(eva_MSE,0)
bob_BER = mean(bob_BER,0)
eva_BER = mean(eva_BER,0)
SC      = mean(SC,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(P,bob_MSE,'ko-',label='Bob')
plt.plot(P,eva_MSE,'k^:',label='Eve')
plt.xlabel('Pilot Amount')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.semilogy(P,bob_BER,'ko-',label='Bob')
plt.semilogy(P,eva_BER,'k^:',label='Eve')
plt.xlabel('Pilot Amount')
plt.ylabel('BER')
plt.title('BER')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.plot(P,SC,'ko-')
plt.xlabel('Pilot Amount')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.show()

print 'Program Finished'