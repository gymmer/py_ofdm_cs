# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,mean

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
P = 36                      # 导频数，P<N
SNR = 20                    # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
iteration = [0,1,2,3,4]

''' 多组取平均 '''
gro_num = 100
ite_num = len(iteration)
lx_MSE  = zeros((gro_num,ite_num))
CS_MSE  = zeros((gro_num,ite_num))
eva_MSE = zeros((gro_num,ite_num))
lx_BER  = zeros((gro_num,ite_num))
CS_BER  = zeros((gro_num,ite_num))
eva_BER = zeros((gro_num,ite_num))
lx_SC   = zeros((gro_num,ite_num))
CS_SC   = zeros((gro_num,ite_num))

for i in range(gro_num):
    for j in range(ite_num):
        print 'Running... Current group: ',i,j
        
        ''' 根据RSSI/Phase产生随机导频图样'''
        pos_A,pos_B,pos_E = agreement(P,{'iteration':iteration[j]})
        
        ''' 发送端 '''
        bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)
        
        ''' 信道传输 '''
        h_ab,H_ab,y_b = transmission(x,L,K,N,Ncp,SNR)
        
        ''' 理想条件下的信道估计'''
        # 合法用户确切知道发送端导频
        h_lx,H_lx,bits_lx,diagram_lx = receiver(y_b,L,K,N,Ncp,pos_A,modulate_type)
    
        ''' 接收端 信道估计'''
        h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,L,K,N,Ncp,pos_B,modulate_type)
        
        ''' 窃听信道 '''
        h_ae,H_ae,y_e = transmission(x,L,K,N,Ncp,SNR)
        
        ''' 非法用户 '''
        h_eva,H_eva,bits_eva,diagram = receiver(y_e,L,K,N,Ncp,pos_E,modulate_type)
        
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
plt.plot(iteration,lx_MSE, 'ko-', label='Bob(Method 1)')
plt.plot(iteration,CS_MSE, 'k^:', label='Bob(Method 2)')
plt.plot(iteration,eva_MSE,'ks--',label='Eve')
plt.xlabel('Iteration')
plt.ylabel('MSE(dB)')
plt.title('MSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(iteration,lx_BER, 'ko-', label='Bob(Method 1)')
plt.semilogy(iteration,CS_BER, 'k^:', label='Bob(Method 2)')
plt.semilogy(iteration,eva_BER,'ks--',label='Eve')
plt.xlabel('Iteration')
plt.ylabel('BER')
plt.title('BER')
plt.legend()

plt.figure(figsize=(8,5))
plt.plot(iteration,lx_SC,'ko-',label='Bob(Method 1)')
plt.plot(iteration,CS_SC,'k^:',label='Bob(Method 2)')
plt.xlabel('Iteration')
plt.ylabel('Capacity(bit/symbol)')
plt.title('Security Capacity')
plt.legend()

print 'Program Finished'