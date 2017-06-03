# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 13:37:31 2016

@author: gymmer
"""

import numpy as np
import matplotlib.pyplot as plt

def plot(h,H,diagram,re_h,re_H,re_diagram):
    ''' 信道冲激响应 '''
    plt.figure(figsize=(9,9))
    plt.subplot(211)
    plt.stem(np.abs(h),'b')
    plt.title('Wireless Sparse Mutipath Channel in T Doamin(h)')
    plt.ylabel('Channel Impulse Response-CIR')
    plt.show()

    plt.subplot(212)
    plt.stem(np.abs(re_h),'g')
    plt.title('Reconstruct h after Channel Estimation(CS/LS)')
    plt.show()
    
    ''' 信道频率响应 '''
    plt.figure(figsize=(9,9))
    plt.subplot(211)
    plt.plot(np.abs(H),'bo-')
    plt.title('Wireless Sparse Mutipath Channel in F Doamin(H)')
    plt.ylabel('Channel Frequency Response')
    plt.show()
    
    plt.subplot(212)
    plt.plot(np.abs(re_H),'go-')        
    plt.title('Reconstruct H after Channel Estimation(CS/LS)')
    plt.show()
    
    ''' 画出星座图 '''  
    plt.figure(figsize=(9,3))
    plt.subplot(121)
    plt.scatter(np.real(diagram),np.imag(diagram))
    plt.title('Constellation diagram of sender')
    plt.xlim(-4,4)
    plt.ylim(-4,4) 
    
    plt.subplot(122)
    plt.scatter(np.real(re_diagram),np.imag(re_diagram))
    plt.title('Constellation diagram of receiver')
    plt.xlim(-4,4)
    plt.ylim(-4,4)