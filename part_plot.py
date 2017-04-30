# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:37:31 2016

@author: gymmer
"""

import numpy as np
import matplotlib.pyplot as plt

def plot(h,H,re_h,re_H,re_h_eva,re_H_eva):
    ''' 信道冲激响应 '''
    plt.figure(figsize=(10,9))
    plt.subplot(311)
    plt.stem(np.abs(h),'b')
    plt.title('Wireless Sparse Mutipath Channel in T Doamin(h)')
    plt.ylabel('Channel Impulse Response-CIR')
    plt.show()

    plt.subplot(312)
    plt.stem(np.abs(re_h),'g')
    plt.title('Reconstruct h after Channel Estimation(CS/LS)')
    plt.show()
    
    plt.subplot(313)
    plt.stem(np.abs(re_h_eva),'r')
    plt.title('Reconstruct h of Invalid User(CS)')
    plt.xlabel('Sampling Point(Time Delay)')
    plt.show()
    
    ''' 信道频率响应 '''
    plt.figure(figsize=(10,9))
    plt.subplot(311)
    plt.plot(np.abs(H),'bo-')
    plt.title('Wireless Sparse Mutipath Channel in F Doamin(H)')
    plt.ylabel('Channel Frequency Response')
    plt.show()
    
    plt.subplot(312)
    plt.plot(np.abs(re_H),'go-')        
    plt.title('Reconstruct H after Channel Estimation(CS/LS)')
    plt.show()
       
    plt.subplot(313)
    plt.plot(np.abs(re_H_eva),'ro-')
    plt.title('Reconstruct H of Invalid User(CS)')
    plt.xlabel('Subcarrier Index')
    plt.show()
    
    ''' 发送、接收序列 
    plt.figure(figsize=(10,9))
    plt.subplot(221)
    plt.plot(np.abs(Xn),'bo-')
    plt.title('X')
    plt.ylabel('Amplitude')
    plt.show()
       
    plt.subplot(222)
    plt.plot(np.abs(np.dot(np.diag(Xn),H)),'ro-')
    plt.title('X*H')
    plt.show()
    
    plt.subplot(223)
    plt.plot(np.abs(No),'yo-')
    plt.title('No')
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.show()
    
    plt.subplot(224)
    plt.plot(np.abs(Y),'go-')
    plt.title('Y=X*H+No')
    plt.xlabel('Frequency')
    plt.show()'''