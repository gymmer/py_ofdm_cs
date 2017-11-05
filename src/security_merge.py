# -*- coding: utf-8 -*-

import numpy as np
from numpy import array,size

def merge(bits_rssi, bits_phase, mtype):
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
        bits = merge_cross(bits_rssi, bits_phase)
    elif mtype == 'and':
        bits = merge_and(bits_rssi, bits_phase)
    elif mtype == 'or':
        bits = merge_or(bits_rssi, bits_phase)
    elif mtype == 'xor':
        bits = merge_xor(bits_rssi, bits_phase)
    return bits

def merge_cross(bitsA, bitsB):
    '''交叉合并(错位混合)'''
    bits = array([],dtype=np.int32)
    length = min(size(bitsA), size(bitsB))
    for i in range(length):
        bits = np.r_[bits,bitsA[i]]
        bits = np.r_[bits,bitsB[i]]
    return bits

def merge_and(bitsA, bitsB):
    '''与合并'''
    bits = array([],dtype=np.int32)
    length = min(size(bitsA), size(bitsB))
    for i in range(length):
        bits = np.r_[bits,bitsA[i]&bitsB[i]]
    return bits

def merge_or(bitsA,bitsB):
    '''或合并'''
    bits = array([],dtype=np.int32)
    length = min(size(bitsA), size(bitsB))
    for i in range(length):
        bits = np.r_[bits,bitsA[i]|bitsB[i]]
    return bits

def merge_xor(bitsA,bitsB):
    '''异或合并'''
    bits = array([],dtype=np.int32)
    length = min(size(bitsA), size(bitsB))
    for i in range(length):
        bits = np.r_[bits,bitsA[i]^bitsB[i]]
    return bits

if __name__=='__main__':
    bitsA = array([0,0,1,1])
    bitsB = array([0,1,0,1])
    print 'merge cross:',merge_cross(bitsA,bitsB)
    print 'merge and:',  merge_and(bitsA,bitsB)
    print 'merge or:',   merge_or(bitsA,bitsB)
    print 'merge xor:',  merge_xor(bitsA,bitsB)