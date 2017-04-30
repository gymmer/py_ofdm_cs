# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:06:28 2016

@author: My402
"""

import os
import matplotlib.pyplot as plt
from numpy import size,zeros
from channel import channel
from channelEstimation import channelEstimation

os.system('cLS')
plt.close('all')

L = 32                      # L:信道长度
K = 6                       # K:稀疏度/多径数，满足:K<<L
N = [32,64,128]             # 训练序列长度/载波数,满足：L<=N
SNR = [0,5,10,15,20,25,30]  # AWGN信道信噪比

''' 时域的信道脉冲响应'''
h = channel(L, K)

''' LS/MMSE/CS信道估计，得MSE/SER
    比较不同的载波数N和信噪比SNR '''
N_num   = size(N)
SNR_num = size(SNR)
CS_MSE   = zeros((N_num,SNR_num))
LS_MSE   = zeros((N_num,SNR_num))
LS_SER   = zeros((N_num,SNR_num))
MMSE_MSE = zeros((N_num,SNR_num))
MMSE_SER = zeros((N_num,SNR_num))

for i in range(N_num):
    (CS_MSE[i,:],LS_MSE[i,:],LS_SER[i,:],MMSE_MSE[i,:],MMSE_SER[i,:])= channelEstimation(K,h,SNR,N[i])
    
plt.figure(figsize=(8,5))
plt.semilogy(SNR,CS_MSE[0,:],'ro-',linewidth=1,label='CS(Min N)')
plt.semilogy(SNR,CS_MSE[1,:],'rp-',linewidth=1.5,label='CS(Mid N)')
plt.semilogy(SNR,CS_MSE[2,:],'rs-',linewidth=2,label='CS(Max N)')
plt.semilogy(SNR,LS_MSE[0,:],'bo-',linewidth=1,label='LS(Min N)')
plt.semilogy(SNR,LS_MSE[1,:],'bp-',linewidth=1.5,label='LS(Mid N)')
plt.semilogy(SNR,LS_MSE[2,:],'bs-',linewidth=2,label='LS(Max N)')
plt.semilogy(SNR,MMSE_MSE[0,:],'go-',linewidth=1,label='MMSE(Min N)')
plt.semilogy(SNR,MMSE_MSE[1,:],'gp-',linewidth=1.5,label='MMSE(Mid N)')
plt.semilogy(SNR,MMSE_MSE[2,:],'gs-',linewidth=2,label='MMSE(Max N)')
plt.xlabel('SNR(dB)')
plt.ylabel('MSE')
plt.title('MSE of CS/LS/MMSE')
plt.legend()

plt.figure(figsize=(8,5))
plt.semilogy(SNR,LS_SER[0,:],'bo-',linewidth=1,label='LS(Min N)')
plt.semilogy(SNR,LS_SER[1,:],'bp-',linewidth=1.5,label='LS(Mid N)')
plt.semilogy(SNR,LS_SER[2,:],'bs-',linewidth=2,label='LS(Max N)')
plt.semilogy(SNR,MMSE_SER[0,:],'go-',linewidth=1,label='MMSE(Min N)')
plt.semilogy(SNR,MMSE_SER[1,:],'gp-',linewidth=1.5,label='MMSE(Mid N)')
plt.semilogy(SNR,MMSE_SER[2,:],'gs-',linewidth=2,label='MMSE(Max N)')
plt.xlabel('SNR(dB)')
plt.ylabel('SER')
plt.title('SER of LS/MMSE')
plt.legend()

print 'Program Finished'