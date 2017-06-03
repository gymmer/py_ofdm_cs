# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 23:07:17 2016

@author: gymmer
"""

def interlace_code(bits,row,col):
    '''
    bits: 待交织的输入比特流
    row:  矩阵交织器的行数
    col:  矩阵交织器的列数
    应满足 size(bits) = row * col
    '''
    interlace_matrix = bits.reshape(row,col)
    return interlace_matrix.reshape(-1,order='F')
    
def interlace_decode(bits,row,col):
    '''
    bits: 待解交织的输入比特流
    row:  矩阵交织器的行数
    col:  矩阵交织器的列数
    应满足 size(bits) = row * col
    '''
    interlace_matrix = bits.reshape(row,col,order='F')
    return interlace_matrix.reshape(-1)