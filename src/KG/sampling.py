# -*- coding: utf-8 -*-

import sys
import MySQLdb as sql
import matplotlib.pyplot as plt
from numpy import corrcoef,array,pi,zeros,mean,mod
from numpy.random import random

sys.path.append('../')
from util.function import awgn

def sampling_RSSI(sampling_period,sampling_time,corr_ab=0.9,corr_ae=0.4):
    '''
    sampling_period: 采样周期/采样间隔。单位ms。每隔一个采样周期，可采集到一个样本
    sampling_time:   采样时间。单位s。一共采样了这么长的时间，也即每隔一个采样时间，更新一次密钥/导频位置
    corr_ab:         Alice和Bob的信道测量值的相关系数
    corr_ae:         Alice和Eve的信道测量值的相关系数    
                     注：在给定相关系数corr时，得到与samples_A满足corr的samples_B(或samples_E)
    返回值:           采样序列。一共有time/period个采样点。如period=1，time=25，共采样25*1000/1=25000个
    '''
    
    sampling_num = sampling_time*1000/sampling_period
    corr_SNR_dict={
        0.1:10, 0.2:16, 0.3:20, 0.4:23, 0.5:25,
        0.6:27, 0.7:30, 0.8:32, 0.9:36, 1.0:1000 }

    try:
        conn = sql.connect(host='localhost',user='root',passwd='11223',db='rssi',port=3306)
        cur = conn.cursor()       
        sql_script = 'select rssi1 from omni_16dbm where id>0 and id<=%d'%(sampling_num) 
        cur.execute(sql_script)
        samples_A = array(cur.fetchall())
        cur.close()
        conn.close()
    except sql.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        
    samples_B = awgn(samples_A,corr_SNR_dict[corr_ab])
    samples_E = awgn(samples_A,corr_SNR_dict[corr_ae])
    return samples_A,samples_B,samples_E
    
def sampling_phase(sampling_period,sampling_time,corr_ab=0.9,corr_ae=0.4):
    '''
    sampling_period: 采样周期/采样间隔。单位ms。每隔一个采样周期，可采集到一个样本
    sampling_time:   采样时间。单位s。一共采样了这么长的时间，也即每隔一个采样时间，更新一次密钥/导频位置
    corr_ab:         Alice和Bob的信道测量值的相关系数
    corr_ae:         Alice和Eve的信道测量值的相关系数    
                     注：在给定相关系数corr时，得到与samples_A满足corr的samples_B(或samples_E)
    返回值:           采样序列。一共有time/period个采样点。如period=1，time=25，共采样25*1000/1=25000个
    '''
    
    sampling_num = sampling_time*1000/sampling_period
    corr_SNR_dict={
        0.1:6,  0.2:8,  0.3:10, 0.4:12, 0.5:14,
        0.6:17, 0.7:20, 0.8:23, 0.9:29, 1.0:1000 }
    samples_A = 2*pi*random(sampling_num)     # [0,2pi)之间均匀分布
    samples_B = mod(awgn(samples_A,corr_SNR_dict[corr_ab]),2*pi)
    samples_E = mod(awgn(samples_A,corr_SNR_dict[corr_ae]),2*pi)
    return samples_A,samples_B,samples_E

def draw_SNR_corr(stype,sampling_period,sampling_time):
        
    SNR = range(0,51,1)    
    group = 100
    SNR_num = len(SNR)
    corr = zeros((group,SNR_num))
    if stype == 'RSSI':
        samples_A,temp,temp = sampling_RSSI(sampling_period,sampling_time)
    elif stype == 'Phase':
        samples_A,temp,temp = sampling_phase(sampling_period,sampling_time)
        
    for i in range(group):
        print 'running...',i
        for j in range(SNR_num):
            samples_B = awgn(samples_A,SNR[j])
            if stype == 'Phase':
                samples_B = mod(samples_B,2*pi)
            corr[i,j] = corrcoef(samples_A,samples_B,rowvar=0)[0,1]
    corr = mean(corr,0)
    
    plt.figure(figsize=(8,5))
    plt.plot(SNR,corr,'bo-')
    plt.xlabel('SNR(dB)')
    plt.ylabel('Corrcoef')
    plt.title('Corrcoef in different SNR for '+stype)

if __name__=='__main__':
    #draw_SNR_corr('RSSI',1,3)
    #draw_SNR_corr('Phase',1,3)
    rssi_A, rssi_B, rssi_E  = sampling_RSSI(1,1)  
    phase_A,phase_B,phase_E = sampling_phase(1,1)
    
    ''' 画出前100个采样点 '''
    plt.figure(figsize=(8,5))
    plt.plot(range(100),rssi_A[0:100],'ko-', label='Alice')
    plt.plot(range(100),rssi_B[0:100],'k^:', label='Bob')
    plt.plot(range(100),rssi_E[0:100],'ks--',label='Eve')
    plt.xlabel('Probes')
    plt.ylabel('RSSI')
    plt.title('RSSI of communication parts(front 100 samples)')
    plt.legend()
    
    plt.figure(figsize=(8,5))
    plt.plot(range(100),phase_A[0:100],'ko-', label='Alice')
    plt.plot(range(100),phase_B[0:100],'k^:', label='Bob')
    plt.plot(range(100),phase_E[0:100],'ks--',label='Eve')
    plt.xlabel('Probes')
    plt.ylabel('Phase')
    plt.title('Phase of communication parts(front 100 samples)')
    plt.legend()