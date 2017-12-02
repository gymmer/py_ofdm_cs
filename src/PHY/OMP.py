# -*- coding: utf-8 -*-

import numpy as np
from numpy import zeros,dot,transpose,size,conjugate,argmax,abs
from numpy.linalg import inv

def OMP(K,y,Phi,Psi):
    
    '''
    y  = Phi*Psi*x
    Y  = X  *W  *h + N
       = X * H + N
    '''                                       

    #正交匹配追踪法重构信号(本质上是L_1范数最优化问题)
    #匹配追踪：找到一个其标记看上去与收集到的数据相关的小波；在数据中去除这个标记的所有印迹；不断重复直到我们能用小波标记“解释”收集到的所有数据。
    m = 2*K                                     # 算法迭代次数(m>=K)，设x是K-sparse的                  
    T = dot(Phi,Psi)                            # 恢复矩阵(测量矩阵*正交反变换矩阵)
    M = size(T,0)
    N = size(T,1)
    
    hat_X = zeros((1,N),np.complex)             # 待重构的谱域(变换域)向量                     
    r_n   = y                                   # 残差值
    pos_array = zeros((m,1))                    # 最大投影系数的位置                          
    product   = zeros((1,N))
    
    for times in range(m):                      # 迭代次数(有噪声的情况下,该迭代次数为K)
        for col in range(N):                    # 恢复矩阵的所有列向量
            product[0,col] = abs(dot(conjugate(T[:,col]),r_n)) # 恢复矩阵的列向量和残差的投影系数(内积值) 
        
        pos   = argmax(product)                 # 最大投影系数对应的位置，即找到一个其标记看上去与收集到的数据相关的小波                   
        if times==0:
            Aug_t = T[:,pos].copy().reshape(M,1)# 增量矩阵
        else:
            Aug_t = np.c_[Aug_t,T[:,pos]]       # 矩阵扩充
           
        T[:,pos] = zeros(M)                     # 选中的列置零（实质上应该去掉，为了简单我把它置零），在数据中去除这个标记的所有印迹
        Aug_t_tr = conjugate(transpose(Aug_t))  # 共轭转置    
        inverse  = inv(dot(Aug_t_tr,Aug_t))
        aug_y    = dot(dot(inverse,Aug_t_tr),y) # 最小二乘,使残差最小          
        r_n      = y-dot(Aug_t,aug_y)           # 残差
        pos_array[times] = pos                  # 纪录最大投影系数的位置
        
    for i in range(m):                          # 重构的谱域向量
        pos = np.int(pos_array[i])
        hat_X[:,pos] = aug_y[i]       
          
    return transpose(hat_X)