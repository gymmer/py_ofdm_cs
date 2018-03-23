# -*- coding: utf-8 -*-

import random
import numpy as np
from numpy import zeros,sqrt,sum,array,shape,nonzero
from numpy.random import randn,randint

def get_random_pilot(N,P):
    ''' 生成随机导频序列 '''
    # 导频插入的位置。取值范围[0,N-1]，不重复的P个随机整数
    pos = random.sample(range(N),P)
    pos.sort()
    return pos

def get_even_pilot(N,interval):
    ''' 生成均匀导频序列 '''
    # 导频插入的位置。取值范围[0,N-1]，间隔为interval
    pos = range(0,N,interval)
    return pos
    
def awgn(X,SNR):
    ''' AWGN信道传输模型 '''
    SNR_log=10**(SNR/10.0)
    xpower=sum(X**2)/len(X)
    npower=xpower/SNR_log
    No=randn(len(X)) * sqrt(npower)
    Y = zeros(X.shape,X.dtype)
    for i in range(len(X)):
        Y[i]=X[i]+No[i]
    return Y

def how_many_equal(arr_A,arr_B):
    ''' 求两个数组中，相同元素的个数 '''
    equal = 0    
    for pos in arr_A:
        if pos in arr_B:
            equal += 1
    return equal

def nonzero_num(vector):
    ''' 求一维向量中非零元素个数 '''
    return shape(nonzero(vector)[0])[0]

def Hw(bits):
    ''' 求二进制序列的汉明重量 '''
    # 非零的元素个数。对于二进制字符串来说，就是1的个数
    return nonzero_num(bits)

def Hd(bits_A,bits_B):
    ''' 求两个二进制序列的汉明距离 '''
    # 通过对应向量（或矩阵）相减，结果中元素中非零元素个数即为汉明距离
    return nonzero_num(bits_A-bits_B)

def guess_pos(N,P,pos,right_num):
    '''
    非法用户随机猜测导频位置。此时传入的pos为发送端的导频图样.
    与pos相比，非法用户猜对了right_num个
    '''
    pos_original = array(pos)                       # 合法用户的导频序列
    where_right = random.sample(range(P),right_num) # 猜对的导频，一共P个导频，从中猜对了right_num个
    
    pos_eva = array([],dtype=np.int32)              # 非法用户随机猜的导频序列，初始化为空
    pos_eva_size = 0                                # 非法导频序列的位置，初始化为0
    while pos_eva_size < P:                         # 先生成一个与合法导频序列完全不同的非法导频序列
        new_pos = randint(low=0,high=N)             # 随机产生一个新的非法导频位置，取值[0,N)
        if (new_pos not in pos) and (new_pos not in pos_eva) : # 新的非法位置，不在合法序列中，也不与已产生的任意非法位置重合
            pos_eva = np.r_[pos_eva,new_pos]        # 只要满足了上述条件，这个新产生的位置才有效，加入到非法导频序列中
            pos_eva_size += 1                       # 更新非法导频序列的长度
    
    pos_eva[where_right] = pos_original[where_right]# 对于那些猜对的位置，更正非法导频序列
    pos_eva.sort()
    return pos_eva