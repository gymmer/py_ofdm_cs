# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 15:18:42 2016

@author: gymmer
"""

import random
import numpy as np
from numpy import zeros,array
import operator

def fac(n):
    ''' 计算阶乘 '''
    if n==0:
        return 1
    else:
        return reduce(operator.mul,range(1,n+1)) 
        
def c(n,m):
    ''' 计算组合数 '''
    return fac(n)/(fac(m)*fac(n-m))
  
def eva_guess_pro(N,P):
    
    ''' 窃听者从N个子载波中，猜测P个导频的位置。
    假设窃听者猜中n个时，其概率为pro，
    则n=0,1,2,...,P时，各有对应的概率
    返回概率分布，以及概率最大的n'''
  
    pro = zeros(P+1,dtype=np.double)     # 猜中的概率
    for i in range(P+1):                 # 猜中的导频数
        pro[i] = c(P,i)*c(N-P,P-i)/(c(N,P)+0.0)
    max_right = np.argmax(pro)           # 找到概率最大对应的位置
    return pro,max_right
    
def guess_pos(N,P,pos,right_num):
        
    pos_original = array(pos)                       # 合法用户的导频序列
    where_right = random.sample(range(P),right_num) # 猜对的导频，一共P个导频，从中猜对了right_num个
    
    pos_eva = array([],dtype=np.int32)              # 非法用户随机猜的导频序列，初始化为空
    pos_eva_size = 0                                # 非法导频序列的位置，初始化为0
    while pos_eva_size < P:                         # 先生成一个与合法导频序列完全不同的非法导频序列
        new_pos = np.random.randint(low=0,high=N)   # 随机产生一个新的非法导频位置，取值[0,N)
        if (new_pos not in pos) and (new_pos not in pos_eva) : # 新的非法位置，不在合法序列中，也不与已产生的任意非法位置重合
            pos_eva = np.r_[pos_eva,new_pos]        # 只要满足了上述条件，这个新产生的位置才有效，加入到非法导频序列中
            pos_eva_size += 1                       # 更新非法导频序列的长度
    
    pos_eva[where_right] = pos_original[where_right]# 对于那些猜对的位置，更正非法导频序列
    pos_eva.sort()
    return pos_eva