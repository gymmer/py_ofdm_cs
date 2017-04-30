# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 13:06:28 2016

@author: My402
"""

import os
from numpy import zeros,mean,arange
import numpy as np
import matplotlib.pyplot as plt
from RSSI_pos_agreement import agreement
from part_sender import sender
from part_transmission import transmission
from part_receiver import receiver
#from part_plot import plot
from function import MSE,BMR
import pdb  
os.system('cls')
plt.close('all')

L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
M = 2                       # 每帧的OFDM符号数
Ncp = 64                    # 循环前缀的长度,Ncp>L
Nt = 1                      # 发送天线数
Nr = 1                      # 接收天线数 
SNR = 30                    # AWGN信道信噪比

''' 根据RSSI产生导频图样'''
P = 36                      # 导频数，P<N
pos_A = np.zeros((Nt,P),dtype=np.int32)
pos_B = np.zeros((Nt,P),dtype=np.int32)
pos_E = np.zeros((Nt,P),dtype=np.int32)
for t in range(Nt):
    pos_A[t,:],pos_B[t,:],pos_E[t,:] = agreement(2,2,P)
    
''' 均匀导频图样
P = 103
pos_A = np.zeros((Nt,P),dtype=np.int32)
pos_B = np.zeros((Nt,P),dtype=np.int32)
pos_E = np.zeros((Nt,P),dtype=np.int32)
for t in range(Nt):
    pos_A[t,:] = arange(P)*5+t
    pos_B[t,:] = arange(P)*5+t
    pos_E[t,:] = arange(P)*5+t'''


''' 发送端 '''
bits_A,SEND = sender(N,M,Ncp,Nt,Nr,pos_A)

''' 信道传输 '''
h,H,RECEIVE = transmission(SEND,L,K,N,M,Ncp,Nt,Nr,SNR)

''' 接收端 信道估计'''
h_cs,H_cs,bits_cs = receiver(RECEIVE,L,K,N,M,Ncp,Nt,Nr,pos_B,'CS')
h_ls,H_ls,bits_ls = receiver(RECEIVE,L,K,N,M,Ncp,Nt,Nr,pos_B,'LS')
h_eva,H_eva,bits_eva = receiver(RECEIVE,L,K,N,M,Ncp,Nt,Nr,pos_E,'CS')

print BMR(bits_A,bits_cs)
print MSE(H[0,0,:],H_cs[0,0,:,0])

''' 信道冲激响应 '''
plt.figure(figsize=(10,9))
plt.subplot(221)
plt.stem(np.abs(h[0,0,:]),'b')
plt.title('H')
plt.ylabel('Channel Impulse Response-CIR')
plt.show()

plt.subplot(222)
plt.stem(np.abs(h_cs[0,0,:,0]),'g')
plt.title('h_cs')
plt.show()

plt.subplot(223)
plt.stem(np.abs(h_ls[0,0,:,1]),'y')
plt.title('h_ls')
plt.show()

plt.subplot(224)
plt.stem(np.abs(h_eva[0,0,:,1]),'r')
plt.title('h_eva')
plt.show()

if Nt==2:
    plt.figure(figsize=(10,9))
    plt.subplot(221)
    plt.stem(np.abs(h[0,1,:]),'b')
    plt.title('H')
    plt.ylabel('Channel Impulse Response-CIR')
    plt.show()
    
    plt.subplot(222)
    plt.stem(np.abs(h_cs[0,1,:,0]),'g')
    plt.title('h_cs')
    plt.show()
    
    plt.subplot(223)
    plt.stem(np.abs(h_ls[0,1,:,1]),'y')
    plt.title('h_ls')
    plt.show()
    
    plt.subplot(224)
    plt.stem(np.abs(h_eva[0,1,:,1]),'r')
    plt.title('h_eva')
    plt.show()

''' 信道频率响应 
plt.figure(figsize=(10,9))
plt.subplot(311)
plt.plot(np.abs(H[0,0,:]),'bo-')
plt.title('Wireless Sparse Mutipath Channel in F Doamin(H)')
plt.ylabel('Channel Frequency Response')
plt.show()

plt.subplot(312)
plt.plot(np.abs(H_cs[0,0,:,0]),'go-')        
plt.title('Reconstruct H after Channel Estimation(CS/LS)')
plt.show()
   
plt.subplot(313)
plt.plot(np.abs(H_cs[0,0,:,1]),'ro-')
plt.title('Reconstruct H of Invalid User(CS)')
plt.xlabel('Subcarrier Index')
plt.show()

plt.figure(figsize=(10,9))
plt.subplot(311)
plt.plot(np.abs(H[0,1,:]),'bo-')
plt.title('Wireless Sparse Mutipath Channel in F Doamin(H)')
plt.ylabel('Channel Frequency Response')
plt.show()

plt.subplot(312)
plt.plot(np.abs(H_cs[0,1,:,0]),'go-')        
plt.title('Reconstruct H after Channel Estimation(CS/LS)')
plt.show()
   
plt.subplot(313)
plt.plot(np.abs(H_cs[0,1,:,1]),'ro-')
plt.title('Reconstruct H of Invalid User(CS)')
plt.xlabel('Subcarrier Index')
plt.show()'''
  
print 'Program Finished'