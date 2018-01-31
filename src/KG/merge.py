# -*- coding: utf-8 -*-

import numpy as np
from numpy import array,size

def merge(bits_rssi,bits_phase,mtype):
    '''
    bits_rssi: 由RSSI量化生成的二进制序列
    bits_phase: 由相位量化生成的二进制序列
    mtype: 合并类型。RSSI/Phase/cross/and/or/xor
    返回值: 合并后的二进制序列
    '''

    if mtype == 'RSSI':
        bits = bits_rssi
    elif mtype == 'Phase':
        bits = bits_phase
    elif mtype == 'cross':
        bits = merge_cross(bits_rssi,bits_phase)
    elif mtype == 'and':
        bits = merge_and(bits_rssi,bits_phase)
    elif mtype == 'or':
        bits = merge_or(bits_rssi,bits_phase)
    elif mtype == 'xor':
        bits = merge_xor(bits_rssi,bits_phase)
    return bits

def merge_cross(bits_A,bits_B):
    '''交叉合并(错位混合)'''
    bits = array([],dtype=np.int32)
    length = min(size(bits_A),size(bits_B))
    for i in range(length):
        bits = np.r_[bits,bits_A[i]]
        bits = np.r_[bits,bits_B[i]]
    return bits

def merge_and(bits_A,bits_B):
    '''与合并'''
    length = min(size(bits_A),size(bits_B))
    bits = bits_A[:length] & bits_B[:length]
    return bits

def merge_or(bits_A,bits_B):
    '''或合并'''
    length = min(size(bits_A),size(bits_B))
    bits = bits_A[:length] | bits_B[:length]
    return bits

def merge_xor(bits_A,bits_B):
    '''异或合并'''
    length = min(size(bits_A),size(bits_B))
    bits = bits_A[:length] ^ bits_B[:length]
    return bits

if __name__=='__main__':
    bits_A = array([1,0,1,1,0,1,0,0])
    bits_B = array([1,0,0,1,0,1,0,1,1,0])
    print 'merge cross:',merge_cross(bits_A,bits_B)
    print 'merge and:',  merge_and(bits_A,bits_B)
    print 'merge or:',   merge_or(bits_A,bits_B)
    print 'merge xor:',  merge_xor(bits_A,bits_B)