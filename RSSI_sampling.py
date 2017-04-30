# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 00:03:32 2016

@author: gymmer
"""

import MySQLdb as sql
from numpy import array
    
def sampling(sampling_period,sampling_time,user_id):
    '''
    sampling_period: 采样周期/采样间隔。单位ms。每隔一个采样周期，可采集到一个RSSI样本
    sampling_time:   采样时间。单位s。一共采样了这么长的时间，也即每隔一个采样时间，更新一次密钥/导频位置
    user_id:         一般的，发送者A_id=1，接收者B_id=2，窃听者E_id=3
    返回值：         RSSI采样序列。一共有time/period个采样点。如period=1，time=25，共采样25*1000/1=25000个RSSI
    '''
    try:
        conn = sql.connect(host='localhost',user='root',passwd='11223',db='rssi',port=3306)
        cur = conn.cursor()
        sampling_num = sampling_time*1000/sampling_period
        sql_script = 'select rssi%d from omni_16dbm where id>0 and id<=%d'%(user_id,sampling_num) 
        cur.execute(sql_script)
        RSSI = cur.fetchall()
        cur.close()
        conn.close()
        return array(RSSI)
    except sql.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])