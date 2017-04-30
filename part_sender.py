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

def sender (N,Ncp,pos):
    
    ''' 二进制序列 '''
    bit_num = N*4         # 总共发送的比特数。对于16QAM，每4个bit编码产生一个星座点，星座点取值[0,15]
    bits = randint(2,size=bit_num)  #随机产生二进制序列
    
    ''' 16-QAM调制 '''
    X = QAM16.mod(bits)     # 16-QAM调制，共产生N个星座点
    
    ''' 画出星座图 
    plt.figure(figsize=(8,5))
    plt.scatter(np.real(X),np.imag(X))
    plt.title('Constellation diagram of sender')
    plt.xlim(-4,4)
    plt.ylim(-4,4)'''
    
    ''' 插入导频,导频位置设为1 '''
    X[pos] = 1
    
    ''' 串并转换 '''
    X = X.reshape(N,1)
    
    ''' IFFT '''
    x = ifft(X,axis=0)
    
    ''' 并串转换 '''
    x = x.reshape(1,N)
    
    ''' 循环前缀 '''
    # 循环前缀的长度Ncp>信道长度L
    cyclic_prefix = x[:,-Ncp:]
    x = np.c_[cyclic_prefix,x]
        
    return bits,x