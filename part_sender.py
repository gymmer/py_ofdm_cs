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

def sender (N,M,Ncp,pos):
   
    ''' 
    N: 子载波数
    M: 每帧的OFDM符号数
    Ncp: 循环前缀长度
    pos: 导频图样
    '''
    
    Nt = 1
    
    ''' 二进制序列 '''
    bit_num = N*M*Nt*4         # 总共发送的比特数。对于16QAM，每4个bit编码产生一个星座点，星座点取值[0,15]
    bits = randint(2,size=bit_num)  #随机产生二进制序列
    
    ''' 16-QAM调制 '''
    X = QAM16.mod(bits)     # 16-QAM调制，共产生N个星座点
    
    ''' 画出星座图 
    plt.figure(figsize=(8,5))
    plt.scatter(np.real(X),np.imag(X))
    plt.title('Constellation diagram of sender')
    plt.xlim(-4,4)
    plt.ylim(-4,4)'''
    
    ''' 串并转换 '''
    # 横坐标代表时域（OFDM符号），纵坐标代表频域（子载波）
    X = X.reshape(N,M)
    
    ''' 插入导频,导频位置设为1 '''
    # 对于频率选择性信道，选择梳状导频图样
    X[pos,:] = 1

    ''' IFFT '''
    x = ifft(X,axis=0)
    
    ''' 循环前缀 '''
    # 循环前缀的长度Ncp>信道长度L
    cyclic_prefix = x[-Ncp:,:]
    x = np.r_[cyclic_prefix,x]
    
    ''' 并串转换 '''
    x = x.reshape(-1,1)
    
    return bits,x