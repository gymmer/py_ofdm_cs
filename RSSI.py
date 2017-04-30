# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 14:08:54 2016

@author: My402
"""
import numpy as np
import matplotlib.pyplot as plt
import MySQLdb as sql
from numpy import random,size,array,mean,std,zeros,ceil
from RC4 import RC4
import tiger
from from_to import from2seq_to10seq,from16_to2seq
import pdb
plt.close('all')

def BMR(bitA,bitB):
    diff = np.abs(bitA-bitB)
    BMR = np.sum(diff)/(size(bitA)+0.0)
    return BMR
    
def sampling(sampling_period,sampling_time,user_id):
    '''
    sampling_period: 采样周期/采样间隔。单位ms。每隔一个采样周期，可采集到一个RSSI样本
    sampling_time:   采样时间。单位s。一共采样了这么长的时间，也即每隔一个采样时间，更新一次密钥/导频位置
    user_id:         一般的，发送者A_id=1，接收者B_id=2，窃听者E_id=3
    返回值：         RSSI采样序列。一共有time/period个采样点。如period=1，time=25，共采样25*1000/1=25000个RSSI
    '''
    try:
        conn = sql.connect(host='localhost',user='root',passwd='402402',db='rssi',port=3306)
        cur = conn.cursor()
        sampling_num = sampling_time*1000/sampling_period
        sql_script = 'select rssi%d from omni_16dbm where id>0 and id<=%d'%(user_id,sampling_num) 
        cur.execute(sql_script)
        RSSI = cur.fetchall()
        cur.close()
        conn.close()
    except sql.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return array(RSSI)
    
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
    
#def generate_SeS(bit_B):
#    Ses = bit_B
#    return Ses
#
#def generate_keyB(SeS,bit_A):
#    bit_B_Aget = SeS
#    return bit_B_Aget
#
#def select_id(bit_A,bit_B,block_num):
#    block_size = size(bit_A)/block_num
#    BMR_AB = zeros(block_num)
#    for i in range(block_num):
#        bit_A_bl = bit_A[i*block_size:(i+1)*block_size]
#        bit_B_bl = bit_B[i*block_size:(i+1)*block_size]
#        BMR_AB[i] = BMR(bit_A_bl,bit_B_bl)
#    optimal_id = np.argmin(BMR_AB)
#    return BMR_AB,optimal_id
#    
#def select_bit_byID(bit,optimal_id,block_num):
#    block_size = size(bit_A)/block_num
#    return bit[optimal_id*block_size:(optimal_id+1)*block_size]
    
def hash_tiger(bit_in):
    # 将二进制序列，以字节为单位，转换成十进制数组
    seq10 = from2seq_to10seq(bit_in)
    
    # 将十进制数组的每个数，转换成ASCII字符，并拼接在一起
    hash_in = ''
    for i in range(size(seq10)):
        hash_in += chr(seq10[i])
    
    # 经hash函数运算，得到48位的十六进制数（字符串表示）
    hash_out = tiger.hash(hash_in)
    
    # 将48位的十六进制，转换成48*4=192位的二进制输出
    bit_out = np.array([],dtype=np.int32)
    for i in range(len(hash_out)):
        current_char = hash_out[i]       
        bit_out = np.r_[bit_out,from16_to2seq[current_char]]
        
    return bit_out

sampling_period,sampling_time = 1,1
RSSI_A = sampling(sampling_period,sampling_time,1)
RSSI_B = sampling(sampling_period,sampling_time,1)+np.random.randint(0,2,size=(1000,1))
RSSI_E = sampling(sampling_period,sampling_time,3)

order,block_num = 2,1
bit_A = quantization(RSSI_A,order,block_num)
bit_B = quantization(RSSI_B,order,block_num)
bit_E = quantization(RSSI_E,order,block_num)
bmr_AB = BMR(bit_A,bit_B)
bmr_AE = BMR(bit_A,bit_E)

key_A = hash_tiger(bit_A)
key_B = hash_tiger(bit_B)
pos_A = RC4(key_A,36)
pos_B = RC4(key_B,36)

plt.figure(figsize=(8,5))
plt.plot(RSSI_A[0:100],'bo-',label='Sender device')
plt.plot(RSSI_B[0:100],'g*-',label='Receiver device')
plt.plot(RSSI_E[0:100],'rp-',label='Eavesdropper')
plt.title('RSSI generated by communication parties(front 100 sampling)')
plt.xlabel('Probes')
plt.ylabel('RSSI(dBm)')
plt.legend()

#plt.figure(figsize=(8,5))
#plt.plot(BMR_AB,'bo',label='Receiver')
#plt.plot(BMR_AE,'rs',label='Eavesdropper')
#plt.plot(optimal_id,BMR_AB[optimal_id],'go',label='optimal_id')
#plt.plot(optimal_id,BMR_AE[optimal_id],'ms')
#plt.plot(range(-1,block_num+2),[0]*(block_num+3),'k-')
#plt.title('BMR of each blocks of AB & AE')
#plt.xlabel('Block id')
#plt.ylabel('BMR')
#plt.xlim(-1,block_num+1)
#plt.ylim(-0.05)
#plt.legend()
