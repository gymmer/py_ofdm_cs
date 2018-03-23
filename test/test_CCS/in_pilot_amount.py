# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean

sys.path.append('../../src')
from util.function import get_random_pilot
from util.metric import MSE,BMR,SecCap
from OFDM import sender,transmission,receiver
  
os.system('cls')
plt.close('all')

''' 参数 '''
N = 512                     # 训练序列长度/载波数,满足：L<=N
P = range(4,60,4)           # 导频数，P<N
SNR = 20                    # AWGN信道信噪比

''' 多组取平均 '''
group_num = 100
P_num     = len(P)
bob_MSE   = zeros((group_num,P_num))
eva_MSE   = zeros((group_num,P_num))
bob_BER   = zeros((group_num,P_num))
eva_BER   = zeros((group_num,P_num))
SC        = zeros((group_num,P_num))

for i in range(group_num):
    for j in range(P_num):
        print 'Running... Current group: ',i,j
        
        pos_A = pos_B = get_random_pilot(N,P[j])
        pos_E = get_random_pilot(N,P[j])
        bits_A,diagram_A,x = sender(pos_A)
        h_ab,H_ab,y_b = transmission(x,SNR)
        h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,pos_B)
        h_ae,H_ae,y_e = transmission(x,SNR)
        h_eva,H_eva,bits_eva,diagram = receiver(y_e,pos_E)
        bob_MSE[i,j] = MSE(H_ab,H_cs)
        eva_MSE[i,j] = MSE(H_ae,H_eva)   
        bob_BER[i,j] = BMR(bits_A,bits_cs)
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