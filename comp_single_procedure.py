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
from part_plot import plot
from function import MSE,BMR,SecCap
  
os.system('cls')
plt.close('all')

L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
Ncp = 60                    # 循环前缀的长度,Ncp>L
SNR = 30                    # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
       
''' 根据RSSI产生导频图样'''
P = 36                      # 导频数，P<N
pos_A,pos_B,pos_E = agreement(2,2,P)

''' 均匀的导频图样 '''
# 导频插入的位置。每5个插入一个导频。取值{0，5，10，...，510}，共P=103个
#P = 103                     # 导频数，P<N
#pos_A = arange(P)*5;pos_B = arange(P)*5;pos_E = arange(P)*5

''' 发送端 '''
bits_A,diagram_A,x = sender(N,Ncp,pos_A,modulate_type)

''' 信道传输 '''
h,H,W,y = transmission(x,L,K,N,Ncp,SNR)

''' 接收端 信道估计'''
h_cs,H_cs,bits_cs,diagram_cs = receiver(y,L,K,N,Ncp,pos_B,modulate_type,'CS','from_pos')
h_ls,H_ls,bits_ls,diagram_ls = receiver(y,L,K,N,Ncp,pos_B,modulate_type,'LS','from_pos')

''' 非法用户 '''
h_eva,H_eva,bits_eva,diagram_eva = receiver(y,L,K,N,Ncp,pos_E,modulate_type,'CS','from_pos')
#h_eva,H_eva,bits_eva,diagram_eva = receiver(y,L,K,N,Ncp,pos_A,modulate_type,'CS','1')
        
''' 评价性能 '''
CS_MSE  = MSE(H,H_cs)
LS_MSE  = MSE(H,H_ls)
eva_MSE = MSE(H,H_eva)
CS_Pe   = BMR(bits_A,bits_cs)
LS_Pe   = BMR(bits_A,bits_ls)
eva_Pe  = BMR(bits_A,bits_eva)
CS_SC   = SecCap(CS_Pe,eva_Pe)

print CS_Pe,eva_Pe,CS_SC
''' 画图 '''
plot(h,H,diagram_A,h_cs,H_cs,diagram_cs,h_eva,H_eva,diagram_eva)
          
print 'Program Finished'