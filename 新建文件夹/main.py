# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:06:28 2016

@author: My402
"""

import os
import matplotlib.pyplot as plt
from sender import sender
from transmission import transmission
from receiver import receiver
from receiver_eva import receiver_eva
from plot import plot
from function import MSE

os.system('cls')
plt.close('all')
#import numpy
#numpy.random.seed(0)
L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 128                     # 训练序列长度/载波数,满足：L<=N
P = 36                      # 导频数，P<N
SNR = [0,5,10,15,20,25,30]  # AWGN信道信噪比

''' 发送端 '''
Xn,pos = sender (N,P)

''' 信道传输 '''
h,H,W,X,Y,No = transmission(Xn,L,K,N,SNR[6])

''' 接收端 信道估计'''
h_cs,H_cs,h_ls,H_ls = receiver(X,Y,W,pos,L,N,K)

''' 非法用户 '''
re_h_eva,re_H_eva = receiver_eva(Y,W,N,K,P)

''' 画图 '''
plot(h,H,h_cs,H_cs,re_h_eva,re_H_eva,Xn,Y,No)

''' 评价性能：MSE '''
CS_MSE = MSE(H,H_cs)
LS_MSE = MSE(H,H_ls)
            
''' LS/MMSE/CS信道估计，得MSE/SER
    比较不同的信噪比SNR '''

    
plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE,'ro-',linewidth=1,label='CS')
plt.plot(SNR,LS_MSE,'bp-',linewidth=1,label='LS')
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE of CS/LS/MMSE')
plt.legend()

print 'Program Finished'