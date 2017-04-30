# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 00:02:45 2016

@author: gymmer
"""

import numpy as np
from numpy import size,array
        
def grayCode_3bit(minimum,interval,value):
    if value>=minimum+0*interval and value<minimum+1*interval:
        return array([0,0,0])
    if value>=minimum+1*interval and value<minimum+2*interval:
        return array([0,0,1])
    if value>=minimum+2*interval and value<minimum+3*interval:
        return array([0,1,1])
    if value>=minimum+3*interval and value<minimum+4*interval:
        return array([0,1,0])
    if value>=minimum+4*interval and value<minimum+5*interval:
        return array([1,1,0])
    if value>=minimum+5*interval and value<minimum+6*interval:
        return array([1,1,1])
    if value>=minimum+6*interval and value<minimum+7*interval:
        return array([1,0,1])
    if value>=minimum+7*interval and value<=minimum+8*interval:
        return array([1,0,0])

def grayCode_2bit(minimum,interval,value):
    if value>=minimum+0*interval and value<minimum+1*interval:
        return array([0,0])
    if value>=minimum+1*interval and value<minimum+2*interval:
        return array([0,1])
    if value>=minimum+2*interval and value<minimum+3*interval:
        return array([1,1])
    if value>=minimum+3*interval and value<=minimum+4*interval:
        return array([1,0])
        
def quantization(RSSI,order,block_num):
    '''
    order: N比特量化，量化阶数
    block_num : 将RSSI划分成num个等长的block
    返回值：bit_stream，量化后的比特流
    '''
    block_size = size(RSSI)/block_num       # 每个block中RSSI的样本数
    bit_stream = array([],dtype=np.int32)

    for i in range(block_num):
        RSSI_bl = RSSI[i*block_size:(i+1)*block_size]   # 每个block中RSSI的样本
        range_bl = np.max(RSSI_bl)-np.min(RSSI_bl)
        interval = range_bl/(2**order+0.0)
        if order==3:            # 对每个样本进行3bit格雷码量化
            for j in range(block_size):
                grayCode = grayCode_3bit(np.min(RSSI_bl),interval,RSSI_bl[j])
                bit_stream = np.r_[bit_stream,grayCode]
        elif order==2:          # 对每个样本进行2bit格雷码量化
            for j in range(block_size):
                grayCode = grayCode_2bit(np.min(RSSI_bl),interval,RSSI_bl[j])
                bit_stream = np.r_[bit_stream,grayCode]
    return bit_stream   