# -*- coding: utf-8 -*-

import sys
import numpy as np
from numpy import size
from numpy.random import randint
from numpy.fft import ifft
from default import *

sys.path.append('../')
from PHY import conv_code,interlace_code,diagram_mod,normal_coef,insert_MIMO_pilot,STBC_code

def sender(pos,N=dN,Ncp=dNcp,M=dM,Nt=dNt,Nr=dNr,modulate=dmodulate):     
    ''' 
    pos:  导频图样
    N:    子载波数
    Ncp:  循环前缀长度
    M:    每帧的OFDM符号数
    Nt:   发送天线数
    Nr:   接收天线数
    modulate: 星座调制
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
    bit_num = N_data*M*modulate                 # 总共发送的比特数.对于16QAM，每4个bit编码产生一个星座点，星座点取值[0,15]
    bits_orginal = randint(2,size=bit_num)      # 随机产生二进制序列
    
    '''  信源编码：卷积码 '''
    bits = bits_orginal.copy()
    bits = conv_code(bits)
    
    ''' 交织 '''
    bits = interlace_code(bits,8,size(bits)/8)

    ''' BPSK/QPSK/16QAM调制 '''
    diagram = diagram_mod(bits,modulate)
    
    ''' 星座点归一化 '''
    X = diagram/normal_coef[modulate]
    
    ''' 串并转换 '''
    X = X.reshape(-1,M)                         # 横坐标代表时域（OFDM符号），纵坐标代表频域（数据子载波）
    
    ''' MIMO空时分组码'''
    X = STBC_code(X,N_data,M,Nt)                # N_data*M*Nt,利用第三维表示不同天线发送的OFDM符号

    ''' 对每个天线分别进行OFDM调制 '''
    for t in range(Nt):

        ''' 第t个天线的发送符号 '''
        X_t = X[:,:,t]

        ''' 插入导频 '''   
        X_t = insert_MIMO_pilot(X_t,t,pos)      # 对于频率选择性信道，选择梳状导频图样
    
        ''' IFFT '''
        x_t = ifft(X_t,axis=0)
        
        ''' 循环前缀 '''
        cyclic_prefix = x_t[-Ncp:,:]            # 循环前缀的长度Ncp>信道长度L
        x_t = np.r_[cyclic_prefix,x_t]
        
        ''' 并串转换 '''
        x_t = x_t.reshape(-1,1)

        ''' Nt个天线发送的数据 '''
        if t==0:                                # 每一列代表一个天线发送的调制后的OFDM数据
            x = x_t
        else:
            x = np.c_[x,x_t]

    return bits_orginal,diagram,x