# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 20:38:59 2016

@author: My402
"""

import numpy as np
from numpy import zeros,size,array

from16_to2seq = {'0':array([0,0,0,0]),'1':array([0,0,0,1]),
                 '2':array([0,0,1,0]),'3':array([0,0,1,1]),
                 '4':array([0,1,0,0]),'5':array([0,1,0,1]),
                 '6':array([0,1,1,0]),'7':array([0,1,1,1]),
                 '8':array([1,0,0,0]),'9':array([1,0,0,1]),
                 'A':array([1,0,1,0]),'B':array([1,0,1,1]),
                 'C':array([1,1,0,0]),'D':array([1,1,0,1]),
                 'E':array([1,1,1,0]),'F':array([1,1,1,1]),}
                 
def from2seq_to10(seq2):
    # 将二进制序列转换成十进制
    seq2_bit = size(seq2)
    number10 = 0
    for i in range(seq2_bit):
        number10 += 2**i*seq2[-1-i]
    return number10

def from2seq_to10seq(seq2):
    # 将二进制流，以字节（8位）为单位，转换成十进制数组
    seq2_byte = size(seq2)/8  # 单位：字节
    seq10 = zeros(seq2_byte,np.int32)
    for i in range(seq2_byte):
        seq10[i] = from2seq_to10(seq2[i*8:(i+1)*8])
    return seq10