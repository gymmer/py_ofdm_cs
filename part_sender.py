# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 12:53:23 2016

@author: My402
"""

import numpy as np
from numpy import size
from numpy.random import randint
from numpy.fft import ifft
import matplotlib.pyplot as plt
from OFDM_interlace import interlace_code
from OFDM_diagram import diagram_mod,normal_coef
from OFDM_pilot import insert_pilot
from STBC import STBC_code

def sender (N,M,Ncp,Nt,Nr,pos,modulate_type):     
    ''' 
    N: 子载波数
    M: 每帧的OFDM符号数
    Ncp: 循环前缀长度
    Nt: 发送天线数
    Nr: 接收天线数
    pos: 导频图样
    modulate_type: 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
    '''
    
    ''' 传输数据的子载波数 '''
    # 对于SISO：
    #     数据子载波数 = 总的子载波数 - 导频所占的载波数
    #     频谱利用率  = 数据子载波数 / 总的子载波数
    # pos的结构：Nt*P.每行代表不同发射天线上的导频位置
    # 对于Nt个天线，为了保证子载波正交，当某个天线插入导频时，其他天线的导频位置设为0。
    # 因此：对于MIMO：
    #     数据子载波数 = 总的子载波数 - 导频所占的载波数*天线数
    P = size(pos,axis=0)
    N_data = N-Nt*P

    ''' 二进制序列 '''
    bit_num = N_data*M*modulate_type    # 总共发送的比特数
    bits = randint(2,size=bit_num)      # 随机产生二进制序列

    ''' 交织 '''
    interlace_bits = interlace_code(bits,8,size(bits)/8)

    ''' BPSK/QPSK/16QAM调制 '''
    diagram = diagram_mod(interlace_bits,modulate_type)
    
    ''' 画出星座图 
    plt.figure(figsize=(8,5))
    plt.scatter(np.real(diagram),np.imag(diagram))
    plt.title('Constellation diagram of sender')
    plt.xlim(-4,4)
    plt.ylim(-4,4)'''
    
    ''' 星座点归一化 '''
    diagram = diagram/normal_coef[modulate_type]
    
    ''' 串并转换 '''
    # 横坐标代表时域（OFDM符号），纵坐标代表频域（数据子载波）
    symbol = diagram.reshape(-1,M)
    
    ''' MIMO空时分组码'''
    # N_data*M*Nt,利用第三维表示不同天线发送的OFDM符号
    MIMO = STBC_code(symbol,N_data,M,Nt)

    ''' 对每个天线分别进行OFDM调制 '''
    for t in range(Nt):

        ''' 第t个天线的发送符号 '''
        X = MIMO[:,:,t]

        ''' 插入导频 '''   
        # 对于频率选择性信道，选择梳状导频图样
        X = insert_pilot(X,t,pos)
    
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