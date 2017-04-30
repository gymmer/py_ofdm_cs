# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 08:31:23 2016

@author: My402
"""

import numpy as np
from numpy import shape,zeros,size

def insert_pilot(X,pos):
    ''' 
    X:   数据子载波。N_data*M，不同的列代表多个OFDM符号
    pos: 导频图样。
    N_data = N-P
    '''

    N_data = size(X)
    P = size(pos)
    N = N_data + P

    # 对于频率选择性信道，选择梳状导频图样
    Y = zeros(N,dtype=X.dtype)  # 插入导频后的OFDM符号。N*M
    data_index = 0
    for N_index in range(N):
        if N_index in pos:
            Y[N_index] = 1
        else:
            Y[N_index] = X[data_index]
            data_index += 1
    return Y

def remove_pilot(Y,pos):
    ''' 
    Y:   第r个接收天线上的子载波。N*M，不同的列代表多个OFDM符号
    pos: 导频图样。P*Nt.每列代表不同发射天线上的导频位置
    '''
    Y = Y.reshape(-1)
    N = size(Y)
    P = size(pos)
    N_data = N-P    
    
    X = zeros(N_data,dtype=Y.dtype)  # 移除导频后的OFDM符号。N_data*M
    data_index = 0
    for N_index in range(N):
        if N_index not in pos:
            X[data_index] = Y[N_index]
            data_index += 1
    return X