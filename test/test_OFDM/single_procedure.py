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

''' 参数 '''
L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
Ncp = 64                    # 循环前缀的长度,Ncp>L
modulate = 4                # 星座调制
P = 36                      # 导频数，P<N
SNR = 20                    # AWGN信道信噪比
       
''' 根据RSSI/Phase产生随机导频图样'''
pos_A,pos_B,pos_E = agreement(P)

''' 发送端 '''
bits_A,diagram_A,x = sender(pos_A,N,Ncp,modulate)

''' 信道传输 '''
h_ab,H_ab,y_b = transmission(x,SNR,L,K,N,Ncp)

''' 理想条件下的信道估计'''
# 合法用户确切知道发送端导频
h_lx,H_lx,bits_lx,diagram_lx = receiver(y_b,pos_A,'CS','from_pos',L,K,N,Ncp,modulate)

''' 接收端 信道估计'''
h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,pos_B,'CS','from_pos',L,K,N,Ncp,modulate)

''' 窃听信道 '''
h_ae,H_ae,y_e = transmission(x,SNR,L,K,N,Ncp)

''' 非法用户 '''
h_eva,H_eva,bits_eva,diagram_eva = receiver(y_e,pos_E,'CS','from_pos',L,K,N,Ncp,modulate)
        
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