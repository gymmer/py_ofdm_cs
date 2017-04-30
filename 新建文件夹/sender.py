# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 12:53:23 2016

@author: My402
"""

from numpy.random import randn
import random

def sender (N,P):
    
    '''
    N: 训练序列长度/载波数,满足：L<=N
    P: 导频数，满足P<N
    '''
    
    ''' 发送端序列的频谱Xn '''
    Xn = randn(N)           # 均值为0，方差为1的正态分布
    # 假设采用BPSK调制，符号为+1/-1
    #Xn = randint(low=0,high=2,size=N)*2-1
        
    ''' 导频位置 ''' 
    pos = random.sample(range(N),P)    # 导频插入的位置。取值范围[0,N-1]，不重复的P个随机整数
    pos.sort()
    
    ''' 插入导频,导频位置设为1 '''
    Xn[pos] = 1
    
    return Xn,pos