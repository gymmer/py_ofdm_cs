# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 14:08:54 2016

@author: My402
"""
import numpy as np
from numpy import array,size


def LFSR_work(seq,sign):
    LFSR_num = size(seq)
    # 根据寄存器的类型，选择不同的新增状态
    if sign=='X':
        t = seq[13]^seq[16]^seq[17]^seq[18]
    elif sign=='Y':
        t = seq[20]^seq[21]
    elif sign=='Z':
        t = seq[7]^seq[20]^seq[21]^seq[22]  
    
    # 寄存器移位
    for i in range(LFSR_num-1,0,-1):
        seq[i] = seq[i-1]
    seq[0] = t

def maj(x,y,z):
    # 多数投票函数，如果x,y,z多数为0，则返回0；否则返回1
    t = x+y+z
    if t==0 or t==1:
        return 0
    elif t==2 or t==3:
        return 1

def cal_pos(seq):
    # 将二进制序列转换成十进制
    seq_bit = size(seq)
    pos = 0
    for i in range(seq_bit):
        pos += 2**i*seq[-1-i]
    return pos

def exist(seq,ele):
    # 判断序列中是否存在某个元素。如果存在，返回1；否则返回0
    for i in range(size(seq)):
        if seq[i]==ele:
            return 1
    return 0

def A51(N,P,bit_stream):
    '''
    根据输入的比特流，使用线性移位寄存器产生密钥流，并从密钥流中计算导频位置
    N： 载波数
    P： 导频数
    bit_stream：输入比特流(64位)
    '''
    X_bit,Y_bit,Z_bit = 19,22,23            # 寄存器X、Y、Z分别有19、22、23位
    seed_bit = X_bit+Y_bit+Z_bit            # 寄存器初始种子一共64位
    key_stream = array([],dtype=np.int32)   # 密钥流
    pos = array([],dtype=np.int32)          # 导频的位置序列
   
    seed = bit_stream.copy()                # 初始种子一共64位，取64位输入比特流作为种子
    X = seed[0:X_bit]                       # 分别用充当三个移位寄存器的初始值
    Y = seed[X_bit:X_bit+Y_bit]
    Z = seed[X_bit+Y_bit:seed_bit]
    
    key_bit = 0                             # 密钥流的比特数。初始时未产生密钥流，为0
    pos_num = 0                             # 已生成的导频数。初始时未生成导频，为0
    
    while pos_num<P:                        # 循环停止的条件是，已经根据密钥流产生了足够数量的导频位置       
        s = X[18]^Y[21]^Z[22]               # 单独的密钥流的位，通过异或运算产生
        key_stream = np.r_[key_stream,s]    # 将单独为加入到密钥流中
        key_bit += 1                        # 修改密钥流的总比特数
        
        if key_bit%9==0:                    # 如果N=512,则导频位置的取值范围[0,512]，需要对9位二进制转成十进制。
            new_pos = cal_pos(key_stream[-9:])  # 密钥流每读入9个比特，则计算一次新产生的导频位置
            if not exist(pos, new_pos):     # 如果新增导频不在我的已有导频列表中，则加入这个导频
                pos = np.r_[pos,new_pos]    # 如果已有导频列表中已有该导频，则放弃。防止重复加入多个相同的同频位置
                pos_num += 1                # 修改已产生的导频位置数
            
        m = maj(X[8],Y[10],Z[10])           # 三个移位寄存器的工作条件。保证每生成一个密钥位后，X、Y、Z中至少两个内容会发生改变
        if X[8]==m:
            LFSR_work(X,'X')
        if Y[10]==m:
            LFSR_work(Y,'Y')
        if Z[10]==m:
            LFSR_work(Z,'Z')
    
    pos.sort()
    return pos