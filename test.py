# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:06:28 2016

@author: My402
"""

import os
from numpy import zeros,mean,arange
import matplotlib.pyplot as plt
from RSSI_pos_agreement import agreement
from part_sender import sender
from part_transmission import transmission
from part_receiver import receiver
from part_receiver_eva import receiver_eva
from part_plot import plot
from function import MSE,BMR
  
os.system('cls')
plt.close('all')

L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
M = 6                       # 每帧符号数
Ncp = 64                    # 循环前缀的长度,Ncp>L
SNR = 30                    # AWGN信道信噪比
        
''' 根据RSSI产生导频图样'''
P = 36                      # 导频数，P<N
pos_A,pos_B,pos_E = agreement(2,2,P)

''' 均匀导频图样
P=103
pos_A = arange(P)*5
pos_B = arange(P)*5
pos_E = arange(P)*5 '''

''' 发送端 '''
bits_A,x = sender(N,M,Ncp,pos_A)

''' 信道传输 '''
h,H,y = transmission(x,L,K,N,M,Ncp,SNR)

''' 接收端 信道估计'''
h_cs,H_cs,bits_cs = receiver(y,L,K,N,M,Ncp,pos_B,'CS')
h_ls,H_ls,bits_ls = receiver(y,L,K,N,M,Ncp,pos_B,'LS')

''' 非法用户 '''
h_eva,H_eva,bits_eva = receiver_eva(y,L,K,N,M,Ncp,pos_E,'from_pos')

''' 画图 '''
# 只画某一组中，指定SNR时的h,H,X,Y
plot(h,H,h_cs[:,0],H_cs[:,0],h_eva[:,0],H_eva[:,0])
plot(h,H,h_cs[:,1],H_cs[:,1],h_eva[:,1],H_eva[:,1])
print 'Program Finished'