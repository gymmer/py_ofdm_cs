# -*- coding: utf-8 -*-

import sys
import numpy as np
from numpy import size
from numpy.random import randint
from numpy.fft import ifft

sys.path.append('../')
from PHY import conv_code,interlace_code,diagram_mod,normal_coef,insert_OFDM_pilot

def sender (N,Ncp,pos,modulate_type):
    ''' 
    N: 子载波数
    Ncp: 循环前缀长度
    pos: 导频图样
    modulate_type: 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
    '''
    
    ''' 传输数据的子载波数 '''
    # 对于SISO：
    #     数据子载波数 = 总的子载波数 - 导频所占的载波数
    #     频谱利用率  = 数据子载波数 / 总的子载波数
    P = size(pos,axis=0)
    N_data = N-P
    
    ''' 二进制序列 '''
    bit_num = N_data*modulate_type          # 总共发送的比特数。对于16QAM，每4个bit编码产生一个星座点，星座点取值[0,15]
    bits_orginal = randint(2,size=bit_num)  # 随机产生二进制序列
    
    '''  信源编码：卷积码 '''
    bits = bits_orginal.copy()
    bits = conv_code(bits)
    
    ''' 交织 '''
    bits = interlace_code(bits,2,size(bits)/2)

    ''' BPSK/QPSK/16QAM调制 '''
    diagram = diagram_mod(bits,modulate_type)
    
    ''' 星座点归一化 '''
    X = diagram/normal_coef[modulate_type]
    
    ''' 插入导频 '''   
    X = insert_OFDM_pilot(X,pos)            # 对于频率选择性信道，选择梳状导频图样
    
    ''' 串并转换 '''
    X = X.reshape(N,1)
    
    ''' IFFT '''
    x = ifft(X,axis=0)
    
    ''' 并串转换 '''
    x = x.reshape(1,N)
    
    ''' 循环前缀 '''
    cyclic_prefix = x[:,-Ncp:]              # 循环前缀的长度Ncp>信道长度L
    x = np.c_[cyclic_prefix,x]
        
    return bits_orginal,diagram,x