# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 14:08:54 2016

@author: My402
"""
import numpy as np
import matplotlib.pyplot as plt
from numpy import size,array,mean,std,zeros
    
def get_strategy_list(RSSI,a):
    '''
    RSSI: RSSI样本点。本函数不对RSSI样本做任何改动，只是用来生成策略表
    a: 过滤系数。对介于mean-a*std ~ mean+a*std之间的RSSI样本，采取丢弃策略。a越大，被丢弃的样本越多
    '''
    block_size = 25
    block_num = size(RSSI)/block_size    
    strategy_list = zeros(size(RSSI),dtype=np.int32)
    
    for i in range(block_num):
        RSSI_bl = RSSI[i*block_size:(i+1)*block_size]   # 每个block中RSSI的样本
        mean_value = mean(RSSI_bl)                      # 方差
        std_deviation = std(RSSI_bl)                    # 标准差
        threshold_upper = mean_value+a*std_deviation    # 定义高阈值和低阈值
        threshold_lower = mean_value-a*std_deviation

        save_single = array([])
        drop_single = array([])
        for j in range(block_size):
            if RSSI_bl[j]<threshold_upper and RSSI_bl[j]>threshold_lower:
                # 对于介于高阈值和低阈值之间的样本，采取丢弃策略，记为-1
                strategy_list[i*block_size+j] = -1
                drop_single = np.r_[drop_single,j]
            else:
                # 对于其他样本，采取保留策略，记为+1
                strategy_list[i*block_size+j] = 1
                save_single = np.r_[save_single,j]
    
#    plt.figure(figsize=(8,5))
#    plt.scatter(save_single,RSSI_bl[list(save_single)],color='g',label='Saved   RSS measurements')
#    plt.scatter(drop_single,RSSI_bl[list(drop_single)],color='r',label='Dropped RSS meaurements')
#    plt.plot(range(-1,block_size+1),[mean_value]*(block_size+2),'k-')
#    plt.plot(range(-1,block_size+1),[threshold_upper]*(block_size+2),'k--')
#    plt.plot(range(-1,block_size+1),[threshold_lower]*(block_size+2),'k--')
#    plt.text(-0.2,mean_value+0.2,'Mean',color='b')
#    plt.text(-0.2,threshold_upper+0.2,'Upper\nThreshold',color='b')
#    plt.text(-0.2,threshold_lower+0.2,'Lower\nThreshold',color='b')
#    plt.xlim(-1,block_size)
#    plt.title('A sample RSSI quantizer')
#    plt.xlabel('Probes')
#    plt.ylabel('RSSI(dBm)')
#    plt.legend()    
    return strategy_list
    
def preprocess(RSSI,list_A,list_B):
    ''' 过滤掉平均值附近的RSSI样本点 '''
    joint_strategy = list_A + list_B
    # 对于联合策略表中为2的元素，说明A、B都采取了保留的策略。最终予以保留
    # 对于其中为0或-2的元素，说明A、B至少有一方采取了丢弃策略。最终予以全部丢弃
    filter_RSSI = array([],dtype=RSSI.dtype)    # 过滤掉均值后的RSSI样本
    for i in range(size(RSSI)):
        if joint_strategy[i] == 2:
            filter_RSSI = np.r_[filter_RSSI,RSSI[i]]
    
    # 为了后续处理方便（如cascade要求RSSI的样本数需能被块长k1整除），
    # 将filter_RSSI的长度截断为100的整数倍
    return filter_RSSI[0:size(filter_RSSI)-size(filter_RSSI)%100]