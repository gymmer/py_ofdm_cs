# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 12:53:23 2016

@author: My402
"""

import numpy as np
from numpy.random import randint
from numpy.fft import ifft
import matplotlib.pyplot as plt
import QAM16
import STBC

def sender (N,M,Ncp,Nt,Nr,pos):     
    ''' 
    N: 子载波数
    M: 每帧的OFDM符号数
    Ncp: 循环前缀长度
    Nt: 发送天线数
    Nr: 接收天线数
    pos: 导频图样
    '''
    
    ''' 二进制序列 '''
    bit_num = N*M*4         # 总共发送的比特数。对于16QAM，每4个bit编码产生一个星座点，星座点取值[0,15]
    bits = randint(2,size=bit_num)  #随机产生二进制序列
    
    ''' 16-QAM调制 '''
    diagram = QAM16.mod(bits)     # 16-QAM调制，共产生N个星座点
    
    ''' 画出星座图 
    plt.figure(figsize=(8,5))
    plt.scatter(np.real(diagram),np.imag(diagram))
    plt.title('Constellation diagram of sender')
    plt.xlim(-4,4)
    plt.ylim(-4,4)'''
    
    ''' 串并转换 '''
    # 横坐标代表时域（OFDM符号），纵坐标代表频域（子载波）
    symbol = diagram.reshape(N,M)
    
    ''' MIMO空时分组码'''
    # N*M*Nt,利用第三维表示不同天线发送的OFDM符号
    MIMO = STBC.STBC_code(symbol,N,M,Nt)

    ''' 对每个天线分别进行OFDM调制 '''
    for t in range(Nt):

        ''' 第t个天线的发送符号 '''
        X = MIMO[:,:,t]
        
        ''' 插入导频 '''
        # 对于频率选择性信道，选择梳状导频图样
        #X[pos,:] = 1
        for temp in range(Nt):
            if temp==t:
                # 第t个天线的导频位置设为1
                X[pos[temp:],:] = 1
            else:
                # 其他天线的导频位置设为0，保证子载波正交
                X[pos[temp:],:] = 0
        
        ''' IFFT '''
        x = ifft(X,axis=0)
        
        ''' 循环前缀 '''
        # 循环前缀的长度Ncp>信道长度L
        cyclic_prefix = x[-Ncp:,:]
        x = np.r_[cyclic_prefix,x]
        
        ''' 并串转换 '''
        x = x.reshape(-1,1)
    
        ''' Nt个天线发送的数据 '''
        # 每一列代表一个天线发送的调制后的OFDM数据
        if t==0:
            SEND = x
        else:
            SEND = np.c_[SEND,x]
    
    return bits,SEND