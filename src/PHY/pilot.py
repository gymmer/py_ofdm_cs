# -*- coding: utf-8 -*-

import numpy as np
from numpy import zeros,size,shape

def insert_OFDM_pilot(X,pos):
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

def remove_OFDM_pilot(Y,pos):
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

def insert_MIMO_pilot(X,t,pos):
    ''' 
    X:   第t个发送天线上的数据子载波。N_data*M，不同的列代表多个OFDM符号
    t:   第t个天线
    pos: 导频图样。P*Nt.每列代表不同发射天线上的导频位置
    N_data = N-Nt*P
    '''

    N_data,M = shape(X)
    P,Nt = shape(pos)
    N = N_data + P*Nt

    # 第t个天线的导频位置，需将第t个天线的导频位置设为1
    pos_t = pos[:,t].reshape(1,P)
    # 其他天线的导频位置，需将其他天线的导频位置设为0，保证子载波正交
    pos_other = np.c_[ pos[:,0:t], pos[:,(t+1):Nt] ]

    # 对于频率选择性信道，选择梳状导频图样
    Y = zeros((N,M),dtype=X.dtype)  # 插入导频后的OFDM符号。N*M
    data_index = 0
    for N_index in range(N):
        if N_index in pos_t:
            Y[N_index,:] = 1
        elif N_index in pos_other:
            Y[N_index,:] = 0
        else:
            Y[N_index,:] = X[data_index,:]
            data_index += 1
    return Y

def remove_MIMO_pilot(Y,pos):
    ''' 
    Y:   第r个接收天线上的子载波。N*M，不同的列代表多个OFDM符号
    pos: 导频图样。P*Nt.每列代表不同发射天线上的导频位置
    '''
    
    N,M = shape(Y)
    P,Nt = shape(pos)
    N_data = N-P*Nt    
    
    X = zeros((N_data,M),dtype=Y.dtype)  # 移除导频后的OFDM符号。N_data*M
    data_index = 0
    for N_index in range(N):
        if N_index not in pos:
            X[data_index,:] = Y[N_index,:]
            data_index += 1
    return X