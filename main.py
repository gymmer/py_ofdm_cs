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

os.system('cls')
plt.close('all')

L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
M = 8                       # 每帧的OFDM符号数
Ncp = 64                    # 循环前缀的长度,Ncp>L
Nt = 2                      # 发送天线数
Nr = 1                      # 接收天线数 
SNR = 30                    # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM

''' 根据RSSI产生导频图样'''
# 每个发送天线上的导频数为P，Nt个天线需生成互不相同的P*Nt个导频位置
# pos结构：P*Nt.每列代表不同发射天线上的导频位置
P = 36                      # 导频数，P<N
pos_A,pos_B,pos_E = agreement(2,2,P*Nt)
pos_A = pos_A.reshape(P,Nt)
pos_B = pos_B.reshape(P,Nt)
pos_E = pos_E.reshape(P,Nt)
    
''' 均匀导频图样
P = 103
pos_A = zeros((P,Nt),dtype=np.int32)
pos_B = zeros((P,Nt),dtype=np.int32)
pos_E = zeros((P,Nt),dtype=np.int32)
for t in range(Nt):
    pos_A[:,t] = arange(P)*5+t
    pos_B[:,t] = arange(P)*5+t
    pos_E[:,t] = arange(P)*5+t'''


''' 发送端 '''
bits_A,SEND = sender(N,M,Ncp,Nt,Nr,pos_A,modulate_type)

''' 信道传输 '''
h,H,RECEIVE = transmission(SEND,L,K,N,M,Ncp,Nt,Nr,SNR)

''' 接收端 信道估计'''
h_cs,H_cs,bits_cs = receiver(RECEIVE,L,K,N,M,Ncp,Nt,Nr,pos_B,modulate_type,'CS')
h_ls,H_ls,bits_ls = receiver(RECEIVE,L,K,N,M,Ncp,Nt,Nr,pos_B,modulate_type,'LS')
h_eva,H_eva,bits_eva = receiver(RECEIVE,L,K,N,M,Ncp,Nt,Nr,pos_E,modulate_type,'CS')

print BMR(bits_A,bits_cs)
print MSE(H[0,0,:],H_cs[0,0,:,0])

''' 信道冲激响应 '''
plt.figure(figsize=(10,9))
plt.subplot(221)
plt.stem(np.abs(h[0,0,:]),'b')
plt.title('h')
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
    plt.title('h')
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