# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from numpy import abs,real,imag

def plot(h,H,diagram,re_h,re_H,re_diagram):
    
    ''' 稀疏信道模型 '''
    plt.figure(figsize=(8,5))
    plt.stem(abs(h),'k')
    plt.title('Wireless Sparse Mutipath Channel Model')
    plt.xlabel('Channel Length')
    plt.ylabel('CIR')
    plt.show()
    
    ''' 信道冲激响应 '''
    plt.figure(figsize=(9,9))
    plt.subplot(211)
    plt.stem(abs(h),'k')
    plt.title('Wireless Sparse Mutipath Channel in T Doamin(h)')
    plt.ylabel('CIR')
    plt.show()

    plt.subplot(212)
    plt.stem(abs(re_h),'k')
    plt.title('Reconstruct h after Channel Estimation')
    plt.xlabel('Channel Length')
    plt.show()
    
    ''' 信道频率响应 '''
    plt.figure(figsize=(9,9))
    plt.subplot(211)
    plt.plot(abs(H),'ko-')
    plt.title('Wireless Sparse Mutipath Channel in F Doamin(H)')
    plt.ylabel('CFR')
    plt.show()
    
    plt.subplot(212)
    plt.plot(abs(re_H),'ko-')        
    plt.title('Reconstruct H after Channel Estimation')
    plt.xlabel('Channel Length')
    plt.show()
    
    ''' 星座图 '''  
    plt.figure(figsize=(9,3))
    plt.subplot(121)
    plt.scatter(real(diagram),imag(diagram),c='k')
    plt.title('Constellation diagram of sender')
    plt.xlim(-4,4)
    plt.ylim(-4,4) 
    
    plt.subplot(122)
    plt.scatter(real(re_diagram),imag(re_diagram),c='k')
    plt.title('Constellation diagram of receiver')
    plt.xlim(-4,4)
    plt.ylim(-4,4)