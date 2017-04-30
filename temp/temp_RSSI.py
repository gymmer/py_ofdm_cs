# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 00:02:45 2016

@author: gymmer
"""

import numpy as np
from numpy import size,array,mean,std,append,corrcoef,zeros
from RSSI_quantization_nbit import *
from part_transmission import awgn
import MySQLdb as sql
    
def sampling(sampling_period,sampling_time,corr):
    '''
    sampling_period: 采样周期/采样间隔。单位ms。每隔一个采样周期，可采集到一个RSSI样本
    sampling_time:   采样时间。单位s。一共采样了这么长的时间，也即每隔一个采样时间，更新一次密钥/导频位置
    corr:            在给定相关系数corr时，得到与RSSI_A满足corr的RSSI_B(或RSSI_E)
    返回值：         RSSI采样序列。一共有time/period个采样点。如period=1，time=25，共采样25*1000/1=25000个RSSI
    '''
    corr_SNR_dict={
    0.1:10, 0.2:16, 0.3:20, 0.4:23, 0.5:25,
    0.6:27, 0.7:30, 0.8:32, 0.9:36, 1.0:1000
    }
    
    try:
        conn = sql.connect(host='localhost',user='root',passwd='11223',db='rssi',port=3306)
        cur = conn.cursor()
        sampling_num = sampling_time*1000/sampling_period
        sql_script = 'select rssi1 from omni_16dbm where id>0 and id<=%d'%(sampling_num) 
        cur.execute(sql_script)
        RSSI = cur.fetchall()
        cur.close()
        conn.close()
    except sql.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    
    SNR = corr_SNR_dict[corr]
    RSSI = awgn(array(RSSI),SNR)
    return RSSI

def draw_SNR_corr(sampling_period=1,sampling_time=2):
    
    SNR = range(0,51,1)
    SNR_num = len(SNR)
    group = 100
    corr = zeros((group,SNR_num))
    rssi_A = sampling(sampling_period,sampling_time,1.0)
    
    for i in range(group):
        print 'running...',i
        for j in range(SNR_num):
            rssi_B = awgn(rssi_A,SNR[j])
            corr[i,j] = corrcoef(rssi_A,rssi_B,rowvar=0)[0,1]
    corr = mean(corr,0)
    
    plt.figure(figsize=(8,5))
    plt.plot(SNR,corr,'bo-')
    plt.xlabel('SNR')
    plt.ylabel('Corrcoef')
    plt.title('Corrcoef in different SNR')
    
def remain(bits,drop_list_A,drop_list_B):
    drop_list_both = append(drop_list_A,drop_list_B)
    bits_remain = array([],dtype=bits.dtype)
    for i in range(size(bits)):
        if i not in drop_list_both:
            bits_remain = np.r_[bits_remain,bits[i]]
    return bits_remain
  
def quantization_even(RSSI,block_size,qtype,order):
    '''
    block_size : 将RSSI划分成长为block_size的多个block
    qtype:
        gray:均匀量化、格雷编码
        natural：均匀量化、自然编码
    order:量化阶数，order=1，2，3，4
        若order=1，则格雷编码与自然编码等价
    返回值：bit_stream，量化后的比特流
    '''
    if qtype=='natural':
        if order==4:
            quantize = naturalCode_4bit
        elif order==3:
            quantize = naturalCode_3bit
        elif order==2:
            quantize = naturalCode_2bit
        elif order==1:
            quantize = Code_1bit                
    elif qtype=='gray':
        if order==4:
            quantize = grayCode_4bit
        elif order==3:
            quantize = grayCode_3bit
        elif order==2:
            quantize = grayCode_2bit
        elif order==1:
            quantize = Code_1bit
            
    block_num  = size(RSSI)/block_size
    bit_stream = array([],dtype=np.int32)
    
    for i in range(block_num):
        RSSI_bl  = RSSI[i*block_size:(i+1)*block_size]          # 每个block中RSSI的样本
        minimum  = min(RSSI_bl)                                 # 每个block中的最小值
        interval = (max(RSSI_bl)-min(RSSI_bl))/(2.0**order)     # 每个block的量化间隔
        
        for j in range(block_size):
            bit = quantize(minimum,interval,RSSI_bl[j])
            bit_stream = np.r_[bit_stream,bit]
            
    return bit_stream

def quantization_thre(RSSI,block_size,coef):
    '''
    block_size : 将RSSI划分成长为block_size的多个block
    coef:量化系数，上阈值=均值+系数x标准差，下阈值=均值-系数x标准差
        阈值量化时，若para=0，则双阈值等价为单阈值，阈值=均值
    返回值：bit_stream，量化后的比特流
    '''
    # They drop RSS esimates that lie between two thresholds and maintain
    # a list of indices to track the RSS estimates that are dropped.
    # They exchange their list of dropped RSS estimates and 
    # only keep th ones that they both decide not to drop.     
    block_num  = size(RSSI)/block_size
    bit_stream = array([],dtype=np.int32)
    drop_list  = array([],dtype=np.int32)
    
    for i in range(block_num):
        RSSI_bl = RSSI[i*block_size:(i+1)*block_size]       # 每个block中RSSI的样本
        upper = mean(RSSI_bl)+coef*std(RSSI_bl)             # 上阈值
        lower = mean(RSSI_bl)-coef*std(RSSI_bl)             # 下阈值
        
        for j in range(block_size):
            if RSSI_bl[j] >= upper:
                bit_stream = np.r_[bit_stream,1]
            elif RSSI_bl[j] <= lower:
                bit_stream = np.r_[bit_stream,0]
            else:
                bit_stream = np.r_[bit_stream,-100]         # 用来临时填充
                drop_list = np.r_[drop_list,i*block_size+j]
      
    return bit_stream,drop_list