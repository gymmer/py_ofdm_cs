# -*- coding: utf-8 -*-

import numpy as np
import random
from numpy import size,zeros
    
def BINARY(X,Y):
    n = size(X)                  # X(或Y)的二进制序列的长度
    
    if n==1:                     #递归过程执行直到剩余一个比特，这个比特就是错误的比特。将Y的该位改正（即取反）
        Y[0] ^= 1
        return
        
    X_front = X[:n/2]            # 将X一分为二，计算前半部分的奇偶校验值
    par_X_front = np.sum(X_front)%2
    
    Y_front = Y[:n/2]            # 将Y一分为二，计算前半部分的奇偶校验值
    par_Y_front = np.sum(Y_front)%2
    
    if par_X_front==par_Y_front: # 如果对比结果一致，说明错误发生在后半段。对后半段递归执行二分法
        BINARY(X[n/2:],Y[n/2:])
    else:                        # 前半段对比结果不一致，说明错误发生在前半段。对前半段递归执行二分法        
        BINARY(X_front,Y_front)
    
def randfunc(n,ki):
    # 构造随机函数，将n个数据随机映射到BL个组上
    BL = int(n/ki)
    re = random.sample(range(n),n)          # 将n个数据打乱顺序重排
    f = zeros((BL,ki),dtype=np.int32)       # 映射函数
    for i in range(BL):                     # 每ki个映射到一个组上
        f[i,:] = re[i*ki:(i+1)*ki]
        f[i,:].sort()
    return f

def reshape_bits(X,Y,k):
    # 将序列划分成BL个子区间，每个区间长度为k，并对序列做截断，防止不能被整除
    n = size(X)
    BL = int(n/k)
    n = BL*k
    return X[0:n],Y[0:n]

def cascade(bits_A,bits_B,iteration):
    '''
    bits_A: Alice量化生成的密钥
    bits_B: Bob量化生成的密钥
    iteration: 算法迭代次数
    '''
    if iteration == 0:
        return bits_A,bits_B
    
    ''' 第一轮 '''
    inter = 1           # 第几轮迭代
    k1 = 10             # 第一轮的块长度
    bits_A,bits_B = reshape_bits(bits_A,bits_B,k1)
    n = size(bits_A)
    BL = n/k1
    # 划分成BL个block
    K1_A = bits_A.reshape(BL,k1)
    K1_B = bits_B.reshape(BL,k1)
    # 校验位
    par1_A = np.sum(K1_A,axis=1)%2
    par1_B = np.sum(K1_B,axis=1)%2
    # 对校验位不匹配的block进行二分查找，纠正错误
    for v in range(BL):
        if par1_A[v] != par1_B[v]:
            BINARY(K1_A[v,:],K1_B[v,:])       
    K1_A.shape = n
    K1_B.shape = n
    
    if iteration == 1:
        return K1_A,K1_B

    ''' 以后若干轮 '''
    # 为第二轮迭代做准备
    last_k = k1
    last_Ki_A = K1_A
    last_Ki_B = K1_B
    while inter<iteration:
        n = size(last_Ki_A)
        ki = 2*last_k       # 第i轮的块长度i，设为上一轮块长度的2倍
        last_Ki_A,last_Ki_B = reshape_bits(last_Ki_A,last_Ki_B,ki)
        n = size(last_Ki_A)
        BL = n/ki
        f = randfunc(n,ki)  # 随机置换函数
        # 对A、B同时用置换函数重排二进制序列
        Ki_A = zeros((BL,ki),dtype=np.int32)
        Ki_B = zeros((BL,ki),dtype=np.int32)
        for i in range(BL):
            for j in range(ki):
                Ki_A[i,j] = last_Ki_A[f[i,j]]
                Ki_B[i,j] = last_Ki_B[f[i,j]]
        # 校验位       
        pari_A = np.sum(Ki_A,axis=1)%2
        pari_B = np.sum(Ki_B,axis=1)%2
        # 对校验位不匹配的block进行二分查找，纠正错误
        for v in range(BL):
            if pari_A[v] != pari_B[v]:
                BINARY(Ki_A[v,:],Ki_B[v,:])  
        Ki_A.shape = n
        Ki_B.shape = n
        
        # 为下一轮迭代做准备
        last_k = ki
        last_Ki_A = Ki_A
        last_Ki_B = Ki_B
        inter = inter + 1
    # cascade 后，被改正的Ki_A(或Ki_B)与原始的bits_A(或bits_B)相比，被打乱了顺序
    return Ki_A,Ki_B