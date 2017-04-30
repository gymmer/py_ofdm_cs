# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:29:28 2016

@author: gymmer
"""

import random
import numpy as np
from numpy import dot,eye,array,size,zeros
from numpy.fft import fft
import matplotlib.pyplot as plt
from OMP import OMP
from function import fftMatrix
import QAM16

def guess_pos(N,P,pos,right_num):
        
    pos_original = array(pos)                       # 合法用户的导频序列
    where_right = random.sample(range(P),right_num) # 猜对的导频，一共P个导频，从中猜对了right_num个
    
    pos_eva = array([],dtype=np.int32)              # 非法用户随机猜的导频序列，初始化为空
    pos_eva_size = 0                                # 非法导频序列的位置，初始化为0
    while pos_eva_size < P:                         # 先生成一个与合法导频序列完全不同的非法导频序列
        new_pos = np.random.randint(low=0,high=N)   # 随机产生一个新的非法导频位置，取值[0,N)
        if (new_pos not in pos) and (new_pos not in pos_eva) : # 新的非法位置，不在合法序列中，也不与已产生的任意非法位置重合
            pos_eva = np.r_[pos_eva,new_pos]        # 只要满足了上述条件，这个新产生的位置才有效，加入到非法导频序列中
            pos_eva_size += 1                       # 更新非法导频序列的长度
    
    pos_eva[where_right] = pos_original[where_right]# 对于那些猜对的位置，更正非法导频序列
    pos_eva.sort()
    return pos_eva
    
def receiver_eva(y,L,K,N,M,Ncp,pos,guess_type):
    
    '''
    y: 接收信号
    L: 信道长度
    K: 稀疏度
    N: 子载波数
    M: 每帧的OFDM符号数
    Ncp: 循环前缀长度
    pos: 导频图样
    guess_type: 'from_pos' 或 'int型数字'
    '''
    
    P = size(pos)
    
    ''' 假设非法用户用另一个导频图样进行解码 '''
    if guess_type=='from_pos':  # 非法用户使用传入的pos作为导频图样（RSSI量化得到，或均匀放置）       
        pos_eva = pos
    else:                       # 非法用户随机猜测导频位置。此时传入的pos为发送端的导频图样
        right_num = int(guess_type)                 # 与pos相比，非法用户猜对了right_num个
        pos_eva = guess_pos(N,P,pos,right_num)
    
    ''' 串并转换 '''
    y = y.reshape(-1,M)
    
    ''' 移除循环前缀'''
    y = y[Ncp:,:]
    
    
    ''' FFT '''
    Y = fft(y,axis=0)

    ''' 导频选择矩阵 '''
    I = eye(N,N)                # NxN的单位矩阵
    S_eva  = I[pos_eva,:]       # PxN的导频选择矩阵
    
    ''' 提取导频 '''
    Yp_eva = dot(S_eva,Y)       # Px1的导频位置的接受信号向量
    Xp_eva = eye(P,P)           # 非法用户不知道X,但他知道，如果导频位置设为1，Xp实际上就是PxP的单位矩阵  
    W = fftMatrix(N,L)          # 傅里叶正变换矩阵，即：使稀疏的h变为不稀疏的H的基  
    Wp_eva = dot(S_eva,W)       # PxL的矩阵,从W中选取与导频位置对应的P行
     
    ''' CS信道估计 '''
    h_eva = zeros((L,M),dtype=np.complex)   # OMP是时域估计算法，估计得到时域的h
    for i in range(M):                      # 第i个符号的CS重构的h
        h_eva[:,i] = OMP(K,Yp_eva[:,i],Xp_eva,Wp_eva).reshape(L)              
    H_eva = dot(W,h_eva)                    # 傅里叶变换，得到频域的H
   
    ''' 信道均衡 '''
    Y = Y/H_eva

    ''' 并串转换 '''
    Y = Y.reshape(-1,1)
    
    ''' 画出星座图 
    plt.figure(figsize=(8,5))
    plt.scatter(np.real(Y),np.imag(Y))
    plt.title('Constellation diagram of eva')
    plt.xlim(-4,4)
    plt.ylim(-4,4)'''
    
    ''' 16-QAM解调 '''
    bits = QAM16.demod(Y)
    
    return h_eva,H_eva,bits