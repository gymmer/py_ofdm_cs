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
from eva_guess_pro import eva_guess_pro
  
os.system('cls')
plt.close('all')

L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
P = 36                      # 导频数，P<N
SNR = 30                    # AWGN信道信噪比
wrong_num = range(P)

gro_num = 10                # 进行多组取平均
CS_MSE = zeros((gro_num,P))
eva_MSE = zeros((gro_num,P))

for i in range(gro_num):
    for j in range(P):
        ''' 发送端 '''
        Xn,pos = sender (N,P,'random')
        
        ''' 信道传输 '''
        h,H,W,X,Y,No = transmission(Xn,L,K,N,SNR)
        
        ''' 接收端 信道估计'''
        h_cs,H_cs,h_ls,H_ls = receiver(X,Y,W,pos,L,N,K)
        
        ''' 非法用户 '''
        h_eva,H_eva = receiver_eva(Y,W,N,K,P,pos,'%d'%(j))
        
        ''' 评价性能：MSE '''
        CS_MSE[i,j] = MSE(H,H_cs)
        eva_MSE[i,j] = MSE(H,H_eva)
        
        ''' 画图 '''
        # 只画某一组中，指定SNR时的h,H,X,Y
        if i==9 and j==1:
            plot(h,H,h_cs,H_cs,h_eva,H_eva,Xn,Y,No)

''' 多组取平均 '''
CS_MSE = mean(CS_MSE,0)
eva_MSE = mean(eva_MSE,0)

plt.figure(figsize=(8,5))
plt.plot(range(P),CS_MSE,'ro-',label='Valid user')
plt.plot(range(P),eva_MSE,'yo-',label='Eevasdropper')
plt.xlabel('number of right pilots')
plt.ylabel('MSE(dB)')
plt.title('MSE of eevasdropper by random guessing(SNR=%d)'%(SNR))
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
plt.legend()

''' 比较不同的信噪比SNR '''
SNR = [0,5,10,15,20,25,30]  # AWGN信道信噪比
SNR_num = len(SNR)
CS_MSE = zeros((gro_num,SNR_num))
eva_MSE_r = zeros((gro_num,SNR_num))
eva_MSE_2 = zeros((gro_num,SNR_num))
eva_MSE_10 = zeros((gro_num,SNR_num))
eva_MSE_20 = zeros((gro_num,SNR_num))
eva_MSE_25 = zeros((gro_num,SNR_num))
eva_MSE_30 = zeros((gro_num,SNR_num))
eva_MSE_35 = zeros((gro_num,SNR_num))

for i in range(gro_num):
    for j in range(SNR_num):
        ''' 发送端 '''
        Xn,pos = sender (N,P,'random')
        
        ''' 信道传输 '''
        h,H,W,X,Y,No = transmission(Xn,L,K,N,SNR[j])
        
        ''' 接收端 信道估计'''
        h_cs,H_cs,h_ls,H_ls = receiver(X,Y,W,pos,L,N,K)
        
        ''' 非法用户 '''
        h_eva_r,H_eva_r = receiver_eva(Y,W,N,K,P,pos,'random')
        h_eva_2,H_eva_2 = receiver_eva(Y,W,N,K,P,pos,'2')
        h_eva_10,H_eva_10 = receiver_eva(Y,W,N,K,P,pos,'10')
        h_eva_20,H_eva_20 = receiver_eva(Y,W,N,K,P,pos,'20')
        h_eva_25,H_eva_25 = receiver_eva(Y,W,N,K,P,pos,'25')
        h_eva_30,H_eva_30 = receiver_eva(Y,W,N,K,P,pos,'30')
        h_eva_35,H_eva_35 = receiver_eva(Y,W,N,K,P,pos,'35')
        
        ''' 评价性能：MSE '''
        CS_MSE[i,j] = MSE(H,H_cs)
        eva_MSE_r[i,j] = MSE(H,H_eva_r)
        eva_MSE_2[i,j] = MSE(H,H_eva_2)
        eva_MSE_10[i,j] = MSE(H,H_eva_10)
        eva_MSE_20[i,j] = MSE(H,H_eva_20)
        eva_MSE_25[i,j] = MSE(H,H_eva_25)
        eva_MSE_30[i,j] = MSE(H,H_eva_30)
        eva_MSE_35[i,j] = MSE(H,H_eva_35)
        
        ''' 画图 '''
        # 只画某一组中，指定SNR时的h,H,X,Y
        #if i==9 and j==6:
        #    plot(h,H,h_cs,H_cs,h_eva,H_eva,Xn,Y,No)
         
CS_MSE_ave = mean(CS_MSE,0)
eva_MSE_r = mean(eva_MSE_r,0)
eva_MSE_2 = mean(eva_MSE_2,0)
eva_MSE_10 = mean(eva_MSE_10,0)
eva_MSE_20 = mean(eva_MSE_20,0)
eva_MSE_25 = mean(eva_MSE_25,0)
eva_MSE_30 = mean(eva_MSE_30,0)
eva_MSE_35 = mean(eva_MSE_35,0)

plt.figure(figsize=(8,5))
plt.plot(SNR,CS_MSE_ave,'g*-',label='Valid user')
plt.plot(SNR,eva_MSE_r,'ro-',label='EVA(random guess)')
plt.plot(SNR,eva_MSE_2,'y^--',label='EVA(guess 2 right)')
plt.plot(SNR,eva_MSE_10,'g<-.',label='EVA(guess 10 right)')
plt.plot(SNR,eva_MSE_20,'c>:',label='EVA(guess 20 right)')
plt.plot(SNR,eva_MSE_25,'bv-',label='EVA(guess 25 right)')
plt.plot(SNR,eva_MSE_30,'ms--',label='EVA(guess 30 right)')
plt.plot(SNR,eva_MSE_35,'kp:',label='EVA(guess 35 right)')
plt.xlabel('SNR(dB)')
plt.ylabel('MSE(dB)')
plt.title('MSE of eevasdropper by random guessing')
plt.legend()

print 'Program Finished'