# -*- coding: utf-8 -*-

import numpy as np
from numpy import array,size

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