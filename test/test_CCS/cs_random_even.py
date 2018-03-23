# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean

sys.path.append('../../src')
from util.function import get_random_pilot,get_even_pilot
from util.metric import MSE,BMR,SecCap
from OFDM import sender,transmission,receiver
  
os.system('cls')
plt.close('all')

''' 参数 '''
N = 512                     # 训练序列长度/载波数,满足：L<=N
P = 36                      # CS估计导频数，P<N
SNR = range(0,31,5)         # AWGN信道信噪比
ptype = ['Random', 'Even']  # 导频图样的类型

''' 多组取平均 '''
gro_num   = 100
SNR_num   = len(SNR)
ptype_num = len(ptype)
bob_MSE   = zeros((gro_num,SNR_num,ptype_num))
eva_MSE   = zeros((gro_num,SNR_num,ptype_num))
bob_BER   = zeros((gro_num,SNR_num,ptype_num))
eva_BER   = zeros((gro_num,SNR_num,ptype_num))
SC        = zeros((gro_num,SNR_num,ptype_num))

for i in range(gro_num):
    for j in range(SNR_num):
        for k in range(ptype_num):
            print 'Running... Current group: ',i,j,k
            
            if ptype[k] == 'Random':
                pos_A = pos_B = get_random_pilot(N,P)
                pos_E = get_random_pilot(N,P)
            elif ptype[k] == 'Even':
                pos_A = pos_B = pos_E = get_even_pilot(N,15)
            
            bits_A,diagram_A,x = sender(pos_A)
            h_ab,H_ab,y_b = transmission(x,SNR[j])
            h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,pos_B)
            h_ae,H_ae,y_e = transmission(x,SNR[j])
            h_eva,H_eva,bits_eva,diagram = receiver(y_e,pos_E)
            bob_MSE[i,j,k] = MSE(H_ab,H_cs)
            eva_MSE[i,j,k] = MSE(H_ab,H_eva)
            bob_BER[i,j,k] = BMR(bits_A,bits_cs)
            eva_BER[i,j,k] = BMR(bits_A,bits_eva)
            SC[i,j,k]      = SecCap(bob_BER[i,j,k],eva_BER[i,j,k])

bob_MSE = mean(bob_MSE,0)   
eva_MSE = mean(eva_MSE,0)
bob_BER = mean(bob_BER,0)
eva_BER = mean(eva_BER,0)
SC      = mean(SC,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(SNR,bob_MSE[:,0],'ko-',label=ptype[0])
plt.plot(SNR,bob_MSE[:,1],'k^:',label=ptype[1])
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,bob_BER[:,0],'ko-',label=ptype[0])
plt.semilogy(SNR,bob_BER[:,1],'k^:',label=ptype[1])
plt.xlabel('SNR(dB)')
plt.ylabel('BER')
plt.title('BER')
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.plot(SNR,SC[:,0],'ko-',label=ptype[0])
plt.plot(SNR,SC[:,1],'k^:',label=ptype[1])
plt.xlabel('SNR(dB)')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.legend()
plt.show()

print 'Program Finished'