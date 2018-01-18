# -*- coding: utf-8 -*-

import sys
import os
import matplotlib.pyplot as plt
from numpy import zeros,argmax

sys.path.append('../')
from util.mathematics import c

os.system('cls')
plt.close('all')

''' 信道参数 '''
N = 512                     # 训练序列长度/载波数,满足：L<=N
P = 36                      # 导频数，P<N

'''
非法用户猜测导频位置，猜对数的概率
窃听者从N个子载波中，猜测P个导频的位置。
假设窃听者猜中n个时，其概率为pro，则n=0,1,2,...,P时，各有对应的概率
'''
pro = zeros(P+1)            # 猜中的概率
for i in range(P+1):        # 猜中的导频数
    pro[i] = c(P,i)*c(N-P,P-i)/(c(N,P)+0.0)
maxright = argmax(pro)      # 找到概率最大对应的位置

print ('Most probabily guess right:Pro(%d)=%f'%(maxright,pro[maxright]))

''' 画图 '''
plt.figure(figsize=(8,5))
plt.plot(pro,'k.-')
plt.plot(maxright,pro[maxright],'ko')
plt.xlabel('Number of Right Pilots')
plt.ylabel('Probability')
plt.title('Probability of Guessing N Pilots Right')
plt.show()

print 'Program Finished'