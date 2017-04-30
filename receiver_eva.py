# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:29:28 2016

@author: gymmer
"""

import random
import numpy as np
from numpy import dot,eye,array
from OMP import OMP
from function import exist

def guess_pos(N,P,pos,right_num):
        
    pos_original = array(pos)                       # 合法用户的导频序列
    where_right = random.sample(range(P),right_num) # 猜对的导频，一共P个导频，从中猜对了right_num个
    
    pos_eva = array([],dtype=np.int32)              # 非法用户随机猜的导频序列，初始化为空
    pos_eva_size = 0                                # 非法导频序列的位置，初始化为0
    while pos_eva_size < P:                         # 先生成一个与合法导频序列完全不同的非法导频序列
        new_pos = np.random.randint(low=0,high=N)   # 随机产生一个新的非法导频位置，取值[0,N)
        if (not exist(pos,new_pos)) and (not exist(pos_eva,new_pos)) : # 新的非法位置，不在合法序列中，也不与已产生的任意非法位置重合
            pos_eva = np.r_[pos_eva,new_pos]        # 只要满足了上述条件，这个新产生的位置才有效，加入到非法导频序列中
            pos_eva_size += 1                       # 更新非法导频序列的长度
    
    pos_eva[where_right] = pos_original[where_right]# 对于那些猜对的位置，更正非法导频序列
    pos_eva.sort()
    return pos_eva
    
def receiver_eva(Y,W,N,K,P,pos,guess_type):
    
    ''' 假设非法用户用另一个导频图样进行解码 '''
    if guess_type=='random':
        # 非法用户随机猜测的导频位置
        pos_eva = random.sample(range(N),P)     # 导频插入的位置。取值范围[0,N-1]，不重复的P个随机整数
        pos_eva.sort()
    else:
        # 与合法用户的导频图样pos相比，非法用户猜对了right_num个
        right_num = int(guess_type)
        pos_eva = guess_pos(N,P,pos,right_num)

    ''' 导频选择矩阵 '''
    I = eye(N,N)                # NxN的单位矩阵
    S_eva  = I[pos_eva,:]       # PxN的导频选择矩阵
    
    ''' 提取导频 '''
    Yp_eva = dot(S_eva,Y)       # Px1的导频位置的接受信号向量
    Xp_eva = eye(P,P)           # 非法用户不知道X,但他知道，如果导频位置设为1，Xp实际上就是PxP的单位矩阵  
    Wp_eva = dot(S_eva,W)       # PxL的矩阵,从W中选取与导频位置对应的P行
     
    ''' CS信道估计 '''
    h_eva = OMP(K,Yp_eva,Xp_eva,Wp_eva)
    H_eva = dot(W,h_eva)
        
    return h_eva,H_eva