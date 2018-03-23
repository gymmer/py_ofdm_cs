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

''' 信道参数 '''
L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
Ncp = 60                    # 循环前缀的长度,Ncp>L
P = 36                      # 导频数，P<N
SNR = 15                    # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
right = range(P+1)          # 非法用户猜对导频数

''' 多组取平均 '''
group_num = 100
right_num = len(right)
lx_MSE    = zeros((group_num,right_num))
CS_MSE    = zeros((group_num,right_num))
eva_MSE   = zeros((group_num,right_num))
lx_BER    = zeros((group_num,right_num))
CS_BER    = zeros((group_num,right_num))
eva_BER   = zeros((group_num,right_num))
lx_SC     = zeros((group_num,right_num))
CS_SC     = zeros((group_num,right_num))

for i in range(group_num):
    for j in range(right_num):
        print 'Running... Current group: ',i,j
        
        ''' 根据RSSI/Phase产生随机导频图样'''
        pos_A,pos_B,pos_E = agreement(P)
        
        ''' 发送端 '''
        bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
        
        ''' 信道传输 '''
        h_ab,H_ab,y_b = transmission(x,L,K,N,Ncp,SNR)
        
        ''' 理想条件下的信道估计'''
        # 合法用户确切知道发送端导频
        h_lx,H_lx,bits_lx,diagram_lx = receiver(y_b,L,K,N,Ncp,pos_A,modulate_type,'CS','from_pos')

        ''' 接收端 信道估计'''
        h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,L,K,N,Ncp,pos_B,modulate_type,'CS','from_pos')
        
        ''' 窃听信道 '''
        h_ae,H_ae,y_e = transmission(x,L,K,N,Ncp,SNR)
        
        ''' 非法用户 '''
        # 非法用户随机猜测导频位置。与发送端的导频图样pos_A相比，非法用户猜对了j个,j取值[0,P)
        h_eva,H_eva,bits_eva,diagram_eva = receiver(y_e,L,K,N,Ncp,pos_A,modulate_type,'CS','%d'%(j))
        
        ''' 评价性能 '''
        lx_MSE[i,j]  = MSE(H_ab,H_lx)
        CS_MSE[i,j]  = MSE(H_ab,H_cs)
        eva_MSE[i,j] = MSE(H_ae,H_eva)
        lx_BER[i,j]  = BMR(bits_A,bits_lx)
        CS_BER[i,j]  = BMR(bits_A,bits_cs)
        eva_BER[i,j] = BMR(bits_A,bits_eva)
        lx_SC[i,j]   = SecCap(lx_BER[i,j],eva_BER[i,j])
        CS_SC[i,j]   = SecCap(CS_BER[i,j],eva_BER[i,j])

lx_MSE  = mean(lx_MSE,0)
CS_MSE  = mean(CS_MSE,0)
eva_MSE = mean(eva_MSE,0)
lx_BER  = mean(lx_BER,0)
CS_BER  = mean(CS_BER,0)
eva_BER = mean(eva_BER,0)
lx_SC   = mean(lx_SC,0)
CS_SC   = mean(CS_SC,0)

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(right,lx_MSE, 'ko-', label='Bob(Method 1)')
plt.plot(right,CS_MSE, 'k^:', label='Bob(Method 2)')
plt.plot(right,eva_MSE,'ks--',label='Eve')
plt.xlabel('Number of Right Pilots')
plt.ylabel('MSE(dB)')
plt.title('MSE of Random Guessing(SNR=%d)'%(SNR))
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.semilogy(right,lx_BER, 'ko-', label='Bob(Method 1)')
plt.semilogy(right,CS_BER, 'k^:', label='Bob(Method 2)')
plt.semilogy(right,eva_BER,'ks--',label='Eve')
plt.xlabel('Number of Right Pilots')
plt.ylabel('BER')
plt.title('BER of Random Guessing(SNR=%d)'%(SNR))
plt.legend()
plt.show()

plt.figure(figsize=(8,5))
plt.plot(right,lx_SC,'ko-',label='Bob(Method 1)')
plt.plot(right,CS_SC,'k^:',label='Bob(Method 2)')
plt.xlabel('Number of Right Pilots')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity of Random Guessing(SNR=%d)'%(SNR))
plt.legend()
plt.ylim(0,1)
plt.show()

print 'Program Finished'