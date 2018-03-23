# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean

sys.path.append('../../src')
from util.metric import MSE,BMR,SecCap
from KG import agreement
from OFDM import sender,transmission,receiver
  
os.system('cls')
plt.close('all')

''' 参数 '''
P = 36                      # 导频数，P<N
SNR = 20                    # AWGN信道信噪比
order = [1,2,3,4,5]
qtype = ['natural','gray']

''' 多组取平均 '''
group_num = 100
order_num = len(order)
qtype_num = len(qtype)
bob_MSE   = zeros((group_num,order_num,qtype_num))
eva_MSE   = zeros((group_num,order_num,qtype_num))
bob_BER   = zeros((group_num,order_num,qtype_num))
eva_BER   = zeros((group_num,order_num,qtype_num))
SC        = zeros((group_num,order_num,qtype_num))

for i in range(group_num):
    for j in range(order_num):
        for k in range(qtype_num):
            print 'Running... Current group: ',i,j,k
            
            pos_A,pos_B,pos_E = agreement(P,{'order':order[j],'qtype':qtype[k]})
            bits_A,diagram_A,x = sender(pos_A)
            h_ab,H_ab,y_b = transmission(x,SNR)
            h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,pos_B)
            h_ae,H_ae,y_e = transmission(x,SNR)
            h_eva,H_eva,bits_eva,diagram = receiver(y_e,pos_E)
            bob_MSE[i,j,k] = MSE(H_ab,H_cs)
            eva_MSE[i,j,k] = MSE(H_ae,H_eva)   
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
plt.plot(order,bob_MSE[:,0],'ko-',label=qtype[0])
plt.plot(order,bob_MSE[:,1],'k^:',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(order,bob_BER[:,0],'ko-',label=qtype[0])
plt.semilogy(order,bob_BER[:,1],'k^:',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(order,SC[:,0],'ko-',label=qtype[0])
plt.plot(order,SC[:,1],'k^:',label=qtype[1])
plt.xlabel('Quantize Order')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.legend()

print 'Program Finished'