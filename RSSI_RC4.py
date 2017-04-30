# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 11:07:24 2016

@author: My402
"""
import numpy as np
from numpy import zeros,size
from from_to import from2seq_to10seq
    
def swap(seq,i,j):
    temp = seq[i]
    seq[i] = seq[j]
    seq[j] = temp
    
def initial(key):
    S = zeros(256)
    K = zeros(256)
    key_len = size(key)
    for i in range(256):
        S[i] = i
        K[i] = key[i%key_len]
    j=0
    for i in range(256):
        j = (j+S[i]+K[i])%256
        swap(S,i,j)
    
    # 对率先生成的256个密钥流字节弃之不用
    i=j=0
    for temp in range(256):
        i = (i+1)%256
        j = (j+S[i])%256
        swap(S,i,j)
        t = (S[i]+S[j])%256
    return S

def RC4(bit_stream,P):
    key = from2seq_to10seq(bit_stream)  # 从二进制流中，以字节为单位，获得密钥，
                                        # 密钥大小可以是1~256字节之间的任意长度，取决于二进制流的长度
    S = initial(key)                    # 初始化查找表。查找表长度为256，查找表包含0~255的8比特数的一个排列    
    pos = zeros(P,dtype=np.int32)       # 导频的位置序列
    pos_num = i = j = 0
    highest = 0    
    
    while pos_num<P:
        i = (i+1)%256
        j = (j+S[i])%256
        swap(S,i,j)
        t = (S[i]+S[j])%256
        keyStreamByte = S[t]            # RC4每次产生一个字节的密钥流，用来生成导频位置
        new_pos = highest*2**8+keyStreamByte
        highest = keyStreamByte%2       # 导频取值于[0,512)共需要9位二进制，而一个密钥流字节只有8位。
                                        # 这里采用本轮密钥的奇偶，来决定下一轮导频位置的最高位。以保证pos可以取到0~512
        if new_pos not in pos:          # 如果新增导频不在我的已有导频列表中，则加入这个导频
            pos[pos_num] = new_pos      # 如果已有导频列表中已有该导频，则放弃。防止重复加入多个相同的同频位置
            pos_num += 1                # 修改已产生的导频位置数
    
    pos.sort()
    return pos   