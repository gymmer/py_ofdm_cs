# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:06:28 2016

@author: My402
"""

import os
from numpy import zeros,mean
import matplotlib.pyplot as plt
from RSSI_pos_agreement import agreement
from part_sender import sender
from part_transmission import transmission
from part_receiver import receiver
from part_plot import plot
from function import MSE,BMR
from eva_guess import eva_guess_pro
  
os.system('cls')
plt.close('all')

L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
Ncp = 60                    # 循环前缀的长度,Ncp>L
P = 36                      # 导频数，P<N
SNR = 30                    # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM

gro_num = 10                # 进行多组取平均
CS_MSE  = zeros((gro_num,P))
eva_MSE = zeros((gro_num,P))
CS_BER  = zeros((gro_num,P))
eva_BER = zeros((gro_num,P))

for i in range(gro_num):
    for j in range(P):
        
        ''' 根据RSSI产生导频图样'''
        pos_A,pos_B,pos_E = agreement(2,2,P)
        
        ''' 发送端 '''
        bits_A,x = sender(N,Ncp,pos_A,modulate_type)
        
        ''' 信道传输 '''
        h,H,W,y = transmission(x,L,K,N,Ncp,SNR)
        
        ''' 接收端 信道估计'''
        h_cs,H_cs,bits_cs = receiver(y,L,K,N,Ncp,pos_B,modulate_type,'CS','from_pos')
        
        ''' 非法用户 '''
        # 非法用户随机猜测导频位置。与发送端的导频图样pos_A相比，非法用户猜对了j个,j取值[0,P)
        h_eva,H_eva,bits_eva = receiver(y,L,K,N,Ncp,pos_A,modulate_type,'CS','%d'%(j))
        
        ''' 评价性能：MSE/BER '''
        CS_MSE[i,j]  = MSE(H,H_cs)
        eva_MSE[i,j] = MSE(H,H_eva)
        CS_BER[i,j]  = BMR(bits_A,bits_cs)
        eva_BER[i,j] = BMR(bits_A,bits_eva)
        
        ''' 画图 '''
        # 只画某一组中，指定j时的h,H,X,Y
        if i==9 and j==1:
            plot(h,H,h_cs,H_cs,h_eva,H_eva)

''' 多组取平均 '''
CS_MSE  = mean(CS_MSE,0)
eva_MSE = mean(eva_MSE,0)
CS_BER  = mean(CS_BER,0)
eva_BER = mean(eva_BER,0)

plt.figure(figsize=(8,5))
plt.plot(range(P),CS_MSE, 'ro-',label='Valid user')
plt.plot(range(P),eva_MSE,'yo-',label='Eevasdropper')
plt.xlabel('number of right pilots')
plt.ylabel('MSE(dB)')
plt.title('MSE of eevasdropper by random guessing(SNR=%d)'%(SNR))
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(range(P),CS_BER, 'ro-',label='Valid user')
plt.semilogy(range(P),eva_BER,'yo-',label='Eevasdropper')
plt.xlabel('number of right pilots')
plt.ylabel('BER')
plt.title('BER of eevasdropper by random guessing(SNR=%d)'%(SNR))
plt.legend()

''' 非法用户猜测导频位置，猜对数的概率 '''
pro,maxright = eva_guess_pro(N,P)
print ('Most probabily guess right:Pro(%d)=%f'%(maxright,pro[maxright]))
plt.figure(figsize=(8,5))
plt.plot(pro,'bo-')
plt.plot(maxright,pro[maxright],'ro')
plt.xlabel('number of right pilots')
plt.ylabel('probability')
plt.title('Probability of the number of right pilots')

''' 比较不同的信噪比SNR '''
SNR = [0,5,10,15,20,25,30]  # AWGN信道信噪比
SNR_num = len(SNR)
CS_MSE = zeros((gro_num,SNR_num))
eva_MSE_r  = zeros((gro_num,SNR_num))
eva_MSE_2  = zeros((gro_num,SNR_num))
eva_MSE_10 = zeros((gro_num,SNR_num))
eva_MSE_20 = zeros((gro_num,SNR_num))
eva_MSE_25 = zeros((gro_num,SNR_num))
eva_MSE_30 = zeros((gro_num,SNR_num))
eva_MSE_35 = zeros((gro_num,SNR_num))

CS_BER = zeros((gro_num,SNR_num))
eva_BER_r  = zeros((gro_num,SNR_num))
eva_BER_2  = zeros((gro_num,SNR_num))
eva_BER_10 = zeros((gro_num,SNR_num))
eva_BER_20 = zeros((gro_num,SNR_num))
eva_BER_25 = zeros((gro_num,SNR_num))
eva_BER_30 = zeros((gro_num,SNR_num))
eva_BER_35 = zeros((gro_num,SNR_num))

for i in range(gro_num):
    for j in range(SNR_num):
        
        ''' 根据RSSI产生导频图样'''
        pos_A,pos_B,pos_E = agreement(2,2,P)
        
        ''' 发送端 '''
        bits_A,x = sender(N,Ncp,pos_A,modulate_type)
        
        ''' 信道传输 '''
        h,H,W,y = transmission(x,L,K,N,Ncp,SNR[j])
        
        ''' 接收端 信道估计'''
        h_cs,H_cs,bits_cs = receiver(y,L,K,N,Ncp,pos_B,modulate_type,'CS','from_pos')
        
        ''' 非法用户 '''
        h_eva_r, H_eva_r,  bits_eva_r  = receiver(y,L,K,N,Ncp,pos_E,modulate_type,'CS','from_pos')
        h_eva_2, H_eva_2,  bits_eva_2  = receiver(y,L,K,N,Ncp,pos_A,modulate_type,'CS','2')
        h_eva_10,H_eva_10, bits_eva_10 = receiver(y,L,K,N,Ncp,pos_A,modulate_type,'CS','10')
        h_eva_20,H_eva_20, bits_eva_20 = receiver(y,L,K,N,Ncp,pos_A,modulate_type,'CS','20')
        h_eva_25,H_eva_25, bits_eva_25 = receiver(y,L,K,N,Ncp,pos_A,modulate_type,'CS','25')
        h_eva_30,H_eva_30, bits_eva_30 = receiver(y,L,K,N,Ncp,pos_A,modulate_type,'CS','30')
        h_eva_35,H_eva_35, bits_eva_35 = receiver(y,L,K,N,Ncp,pos_A,modulate_type,'CS','35')
        
        ''' 评价性能：MSE/BER '''
        CS_MSE[i,j] = MSE(H,H_cs)
        eva_MSE_r[i,j]  = MSE(H,H_eva_r)
        eva_MSE_2[i,j]  = MSE(H,H_eva_2)
        eva_MSE_10[i,j] = MSE(H,H_eva_10)
        eva_MSE_20[i,j] = MSE(H,H_eva_20)
        eva_MSE_25[i,j] = MSE(H,H_eva_25)
        eva_MSE_30[i,j] = MSE(H,H_eva_30)
        eva_MSE_35[i,j] = MSE(H,H_eva_35)
        
        CS_BER[i,j] = BMR(H,H_cs)
        eva_BER_r[i,j]  = BMR(H,H_eva_r)
        eva_BER_2[i,j]  = BMR(H,H_eva_2)
        eva_BER_10[i,j] = BMR(H,H_eva_10)
        eva_BER_20[i,j] = BMR(H,H_eva_20)
        eva_BER_25[i,j] = BMR(H,H_eva_25)
        eva_BER_30[i,j] = BMR(H,H_eva_30)
        eva_BER_35[i,j] = BMR(H,H_eva_35)
        
        ''' 画图 '''
        # 只画某一组中，指定SNR时的h,H,X,Y
        #if i==9 and j==6:
        #    plot(h,H,h_cs,H_cs,h_eva,H_eva)
         
CS_MSE_ave = mean(CS_MSE,0)
eva_MSE_r  = mean(eva_MSE_r,0)
eva_MSE_2  = mean(eva_MSE_2,0)
eva_MSE_10 = mean(eva_MSE_10,0)
eva_MSE_20 = mean(eva_MSE_20,0)
eva_MSE_25 = mean(eva_MSE_25,0)
eva_MSE_30 = mean(eva_MSE_30,0)
eva_MSE_35 = mean(eva_MSE_35,0)

CS_BER_ave = mean(CS_BER,0)
eva_BER_r  = mean(eva_BER_r,0)
eva_BER_2  = mean(eva_BER_2,0)
eva_BER_10 = mean(eva_BER_10,0)
eva_BER_20 = mean(eva_BER_20,0)
eva_BER_25 = mean(eva_BER_25,0)
eva_BER_30 = mean(eva_BER_30,0)
eva_BER_35 = mean(eva_BER_35,0)

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE_ave,'g*-', label='Valid user')
plt.plot(SNR,eva_MSE_r, 'ro-', label='EVA(random guess)')
plt.plot(SNR,eva_MSE_2, 'y^--',label='EVA(guess 2 right)')
plt.plot(SNR,eva_MSE_10,'g<-.',label='EVA(guess 10 right)')
plt.plot(SNR,eva_MSE_20,'c>:', label='EVA(guess 20 right)')
plt.plot(SNR,eva_MSE_25,'bv-', label='EVA(guess 25 right)')
plt.plot(SNR,eva_MSE_30,'ms--',label='EVA(guess 30 right)')
plt.plot(SNR,eva_MSE_35,'kp:', label='EVA(guess 35 right)')
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE of eevasdropper by random guessing')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,CS_BER_ave,'g*-', label='Valid user')
plt.semilogy(SNR,eva_BER_r, 'ro-', label='EVA(random guess)')
plt.semilogy(SNR,eva_BER_2, 'y^--',label='EVA(guess 2 right)')
plt.semilogy(SNR,eva_BER_10,'g<-.',label='EVA(guess 10 right)')
plt.semilogy(SNR,eva_BER_20,'c>:', label='EVA(guess 20 right)')
plt.semilogy(SNR,eva_BER_25,'bv-', label='EVA(guess 25 right)')
plt.semilogy(SNR,eva_BER_30,'ms--',label='EVA(guess 30 right)')
plt.semilogy(SNR,eva_BER_35,'kp:', label='EVA(guess 35 right)')
plt.xlabel('SNR(dB)')
plt.ylabel('BER')
plt.title('BER of eevasdropper by random guessing')
plt.legend()

print 'Program Finished'