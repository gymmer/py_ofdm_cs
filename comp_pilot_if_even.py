# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:06:28 2016

@author: My402
"""

import os
from numpy import zeros,mean
import matplotlib.pyplot as plt
from sender import sender
from transmission import transmission
from receiver import receiver
from receiver_eva import receiver_eva
from plot import plot
from function import MSE
  
os.system('cls')
plt.close('all')

L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
P = [36,103]                # 导频数，P<N
SNR = [0,5,10,15,20,25,30]  # AWGN信道信噪比

''' 比较不同的信噪比SNR '''
SNR_num = len(SNR)
gro_num = 10        # 进行多组取平均
CS_MSE = zeros((gro_num,SNR_num))
LS_MSE = zeros((gro_num,SNR_num))
eva_MSE = zeros((gro_num,SNR_num))

for i in range(gro_num):
    for j in range(SNR_num):
        ''' 发送端 '''
        Xn,pos = sender (N,P[0],'random')
        
        ''' 信道传输 '''
        h,H,W,X,Y,No = transmission(Xn,L,K,N,SNR[j])
        
        ''' 接收端 信道估计'''
        h_cs,H_cs,h_ls,H_ls = receiver(Y,W,L,N,P[0],K,'random')
        
        ''' 非法用户 '''
        h_eva,H_eva = receiver_eva(Y,W,N,K,P[0],pos,'random')
        
        ''' 评价性能：MSE '''
        CS_MSE[i,j] = MSE(H,H_cs)
        LS_MSE[i,j] = MSE(H,H_ls)
        eva_MSE[i,j] = MSE(H,H_eva)
        
        ''' 画图 '''
        # 只画某一组中，指定SNR时的h,H,X,Y
        if i==9 and j==6:
            plot(h,H,h_cs,H_cs,h_eva,H_eva,Xn,Y,No)
          
CS_MSE_0 = mean(CS_MSE,0)
LS_MSE_0 = mean(LS_MSE,0)
eva_MSE_0 = mean(eva_MSE,0)

for i in range(gro_num):
    for j in range(SNR_num):
        ''' 发送端 '''
        Xn,pos = sender (N,P[1],'even')
        
        ''' 信道传输 ''' 
        h,H,W,X,Y,No = transmission(Xn,L,K,N,SNR[j])
        
        ''' 接收端 信道估计''' 
        h_cs,H_cs,h_ls,H_ls = receiver(Y,W,L,N,P[1],K,'even')
        
        #''' 非法用户 '''
        #h_eva,H_eva = receiver_eva(Y,W,N,K,P[0],pos,'random')
        
        ''' 评价性能：MSE '''
        CS_MSE[i,j] = MSE(H,H_cs)
        LS_MSE[i,j] = MSE(H,H_ls)
        
        #''' 画图 '''
        # 只画某一组中，指定SNR时的h,H,X,Y
        #if i==9 and j==6:
        #    plot(h,H,h_ls,H_ls,h_eva,H_eva,Xn,Y,No)

''' 多组取平均 '''
CS_MSE_1 = mean(CS_MSE,0)
LS_MSE_1 = mean(LS_MSE,0)

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE_0,'go-',label='CS,P=%d,random'%(P[0]))
plt.plot(SNR,LS_MSE_0,'bo-',label='LS,P=%d,random'%(P[0]))
plt.plot(SNR,eva_MSE_0,'ro-',label='eva,P=%d,random'%(P[0]))
plt.plot(SNR,CS_MSE_1,'gp-.',label='CS,P=%d,even'%(P[1]))
plt.plot(SNR,LS_MSE_1,'bp-.',label='LS,P=%d,even'%(P[1]))
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE of CS/LS')
plt.legend()

print 'Program Finished'