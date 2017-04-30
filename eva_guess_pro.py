# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 15:18:42 2016

@author: gymmer
"""

import numpy as np
from numpy import zeros
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