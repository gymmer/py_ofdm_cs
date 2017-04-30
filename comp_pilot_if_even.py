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
from function import MSE,BMR
  
os.system('cls')
plt.close('all')

L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
Ncp = 60                    # 循环前缀的长度,Ncp>L
P = [36,103]                # 导频数，P<N
SNR = [0,5,10,15,20,25,30]  # AWGN信道信噪比

''' 比较不同的信噪比SNR '''
SNR_num = len(SNR)
gro_num = 10        # 进行多组取平均
CS_MSE  = zeros((gro_num,SNR_num))
LS_MSE  = zeros((gro_num,SNR_num))
eva_MSE = zeros((gro_num,SNR_num))
CS_BER  = zeros((gro_num,SNR_num))
LS_BER  = zeros((gro_num,SNR_num))
eva_BER = zeros((gro_num,SNR_num))

for i in range(gro_num):
    for j in range(SNR_num):
        
        ''' 根据RSSI产生导频图样'''
        pos_A,pos_B,pos_E = agreement(2,2,P[0])
        
        ''' 发送端 '''
        bits_A,x = sender(N,Ncp,pos_A)

        ''' 信道传输 '''
        h,H,W,y = transmission(x,L,K,N,Ncp,SNR[j])
        
        ''' 接收端 信道估计'''
        h_cs,H_cs,bits_cs = receiver(y,W,L,N,Ncp,K,pos_B,'CS','from_pos')
        h_ls,H_ls,bits_ls = receiver(y,W,L,N,Ncp,K,pos_B,'LS','from_pos')
        
        ''' 非法用户 '''
        h_eva,H_eva,bits_eva = receiver(y,W,L,N,Ncp,K,pos_E,'CS','from_pos')
        
        ''' 评价性能：MSE '''
        CS_MSE[i,j]  = MSE(H,H_cs)
        LS_MSE[i,j]  = MSE(H,H_ls)
        eva_MSE[i,j] = MSE(H,H_eva)
        CS_BER[i,j]  = BMR(bits_A,bits_cs)
        LS_BER[i,j]  = BMR(bits_A,bits_ls)
        eva_BER[i,j] = BMR(bits_A,bits_eva)
        
        ''' 画图 '''
        # 只画某一组中，指定SNR时的h,H,X,Y
        if i==9 and j==6:
            plot(h,H,h_cs,H_cs,h_eva,H_eva)
          
CS_MSE_0  = mean(CS_MSE,0)
LS_MSE_0  = mean(LS_MSE,0)
eva_MSE_0 = mean(eva_MSE,0)
CS_BER_0  = mean(CS_BER,0)
LS_BER_0  = mean(LS_BER,0)
eva_BER_0 = mean(eva_BER,0)

for i in range(gro_num):
    for j in range(SNR_num):
        
        ''' 均匀的导频图样 '''
        # 导频插入的位置。每5个插入一个导频。取值{0，5，10，...，510}，共P=103个
        pos = arange(P[1])*5
        
        ''' 发送端 '''
        bits_A,x = sender(N,Ncp,pos)
        
        ''' 信道传输 ''' 
        h,H,W,y = transmission(x,L,K,N,Ncp,SNR[j])
        
        ''' 接收端 信道估计''' 
        h_cs,H_cs,bits_cs = receiver(y,W,L,N,Ncp,K,pos,'CS','from_pos')
        h_ls,H_ls,bits_ls = receiver(y,W,L,N,Ncp,K,pos,'LS','from_pos')
        
        ''' 非法用户 '''
        # 均匀放置导频时，非法用户可以很容易猜到导频图样。假设非法用户猜到了每5个插入一个导频
        # 这个时候，非法用户的重构性能，和基于CS的合法用户的重构性能，是完全一样的
        h_eva,H_eva,bits_eva = receiver(y,W,L,N,Ncp,K,pos,'CS','from_pos')
        
        ''' 评价性能：MSE '''
        CS_MSE[i,j]  = MSE(H,H_cs)
        LS_MSE[i,j]  = MSE(H,H_ls)
        eva_MSE[i,j] = MSE(H,H_eva)
        CS_BER[i,j]  = BMR(bits_A,bits_cs)
        LS_BER[i,j]  = BMR(bits_A,bits_ls)
        eva_BER[i,j] = BMR(bits_A,bits_eva)
        
        ''' 画图 '''
        # 只画某一组中，指定SNR时的h,H,X,Y
        if i==9 and j==6:
            plot(h,H,h_ls,H_ls,h_eva,H_eva)

''' 多组取平均 '''
CS_MSE_1  = mean(CS_MSE,0)
LS_MSE_1  = mean(LS_MSE,0)
eva_MSE_1 = mean(eva_MSE,0)
CS_BER_1  = mean(CS_BER,0)
LS_BER_1  = mean(LS_BER,0)
eva_BER_1 = mean(eva_BER,0)

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE_0, 'go-' ,label='CS,P=%d,RSSI'%(P[0]))
plt.plot(SNR,LS_MSE_0, 'bo-' ,label='LS,P=%d,RSSI'%(P[0]))
plt.plot(SNR,eva_MSE_0,'rp-' ,label='eva,P=%d,RSSI'%(P[0]))
plt.plot(SNR,CS_MSE_1, 'g+-.',label='CS,P=%d,even'%(P[1]))
plt.plot(SNR,LS_MSE_1, 'b+-.',label='LS,P=%d,even'%(P[1]))
plt.plot(SNR,eva_MSE_1,'r*-.',label='eva,P=%d,even\nsame as CS'%(P[1]))
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE of CS/LS')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,CS_BER_0, 'go-' ,label='CS,P=%d,RSSI'%(P[0]))
plt.semilogy(SNR,LS_BER_0, 'bo-' ,label='LS,P=%d,RSSI'%(P[0]))
plt.semilogy(SNR,eva_BER_0,'rp-' ,label='eva,P=%d,RSSI'%(P[0]))
plt.semilogy(SNR,CS_BER_1, 'g+-.',label='CS,P=%d,even'%(P[1]))
plt.semilogy(SNR,LS_BER_1, 'b+-.',label='LS,P=%d,even'%(P[1]))
plt.semilogy(SNR,eva_BER_1,'r*-.',label='eva,P=%d,even\nsame as CS'%(P[1]))
plt.xlabel('SNR(dB)')
plt.ylabel('BER')
plt.title('BER of CS/LS')
plt.legend()

print 'Program Finished'