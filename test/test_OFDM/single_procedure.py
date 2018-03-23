# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt

sys.path.append('../../src')
from util.metric import MSE,BMR,SecCap
from util.plot import plot
from KG import agreement
from OFDM import sender,transmission,receiver

os.system('cls')
plt.close('all')

''' 信道参数 '''
L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
P = 36                      # 导频数，P<N
Ncp = 60                    # 循环前缀的长度,Ncp>L
SNR = 30                    # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
       
''' 根据RSSI/Phase产生随机导频图样'''
pos_A,pos_B,pos_E = agreement(P)

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
h_eva,H_eva,bits_eva,diagram_eva = receiver(y_e,L,K,N,Ncp,pos_E,modulate_type)
        
''' 评价性能 '''
lx_MSE  = MSE(H_ab,H_lx)
CS_MSE  = MSE(H_ab,H_cs)
eva_MSE = MSE(H_ae,H_eva)

lx_BER  = BMR(bits_A,bits_lx)
CS_BER  = BMR(bits_A,bits_cs)
eva_BER = BMR(bits_A,bits_eva)

lx_SC   = SecCap(lx_BER,eva_BER)
CS_SC   = SecCap(CS_BER,eva_BER)

''' 打印信息 '''
print lx_MSE,CS_MSE,eva_MSE
print lx_BER,CS_BER,eva_BER
print lx_SC,CS_SC

''' 画图 '''
plot(h_ab,H_ab,diagram_A,h_cs,H_cs,diagram_cs)
plot(h_ae,H_ae,diagram_A,h_eva,H_eva,diagram_eva)  

print 'Program Finished'