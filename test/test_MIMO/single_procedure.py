# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt

sys.path.append('../../src')
from util.metric import MSE,BMR,SecCap
from util.plot import plot
from KG import agreement
from MIMO import sender,transmission,receiver

os.system('cls')
plt.close('all')

''' 信道参数 '''
L = 50                      # 信道长度
K = 6                       # 稀疏度/多径数，满足:K<<L
N = 512                     # 训练序列长度/载波数,满足：L<=N
P = 36                      # 导频数，P<N
Ncp = 64                    # 循环前缀的长度,Ncp>L
SNR = 30                    # AWGN信道信噪比
modulate_type = 4           # 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
M = 8                       # 每帧的OFDM符号数
Nt = 2                      # 发送天线数
Nr = 1                      # 接收天线数 

''' 根据RSSI/Phase产生导频图样'''
# 每个发送天线上的导频数为P，Nt个天线需生成互不相同的P*Nt个导频位置
# pos结构：P*Nt.每列代表不同发射天线上的导频位置
pos_A,pos_B,pos_E = agreement(P*Nt)
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
bits_A,diagram_A,x = sender(N,M,Ncp,Nt,Nr,pos_A,modulate_type)

''' 信道传输 '''
h_ab,H_ab,y_b = transmission(x,L,K,N,M,Ncp,Nt,Nr,SNR)

''' 理想条件下的信道估计'''
# 合法用户确切知道发送端导频
h_lx,H_lx,bits_lx,diagram_lx = receiver(y_b,L,K,N,M,Ncp,Nt,Nr,pos_A,modulate_type)

''' 接收端 信道估计'''
h_cs,H_cs,bits_cs,diagram_cs = receiver(y_b,L,K,N,M,Ncp,Nt,Nr,pos_B,modulate_type)
 
''' 窃听信道 '''
h_ae,H_ae,y_e = transmission(x,L,K,N,M,Ncp,Nt,Nr,SNR)

''' 非法用户 '''
h_eva,H_eva,bits_eva,diagram_eva = receiver(y_e,L,K,N,M,Ncp,Nt,Nr,pos_E,modulate_type)

''' 评价性能 '''
lx_MSE  = MSE(H_ab[0,0,:],H_lx[0,0,:,0])
CS_MSE  = MSE(H_ab[0,0,:],H_cs[0,0,:,0])
eva_MSE = MSE(H_ae[0,0,:],H_eva[0,0,:,0])

lx_BER  = BMR(bits_A,bits_lx)
CS_BER  = BMR(bits_A,bits_cs)
eva_BER = BMR(bits_A,bits_eva)

lx_SC   = SecCap(lx_BER,eva_BER)
CS_SC   = SecCap(CS_BER,eva_BER)

''' 打印信息 '''
print lx_MSE,CS_MSE,eva_MSE
print lx_BER,CS_BER,eva_BER
print lx_SC,CS_SC

''' 画图 '''
# 第一个发送天线
plot(h_ab[0,0,:],H_ab[0,0,:],diagram_A,h_cs[0,0,:,0],H_cs[0,0,:,0],diagram_cs)
# 第二个发送天线
plot(h_ab[0,1,:],H_ab[0,1,:],diagram_A,h_cs[0,1,:,0],H_cs[0,1,:,0],diagram_cs)
# 窃听用户
plot(h_ae[0,0,:],H_ae[0,0,:],diagram_A,h_eva[0,0,:,0],H_eva[0,0,:,0],diagram_eva)