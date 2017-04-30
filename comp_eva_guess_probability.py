# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 13:40:53 2016

@author: gymmer
"""

import matplotlib.pyplot as plt
from eva_guess import eva_guess_pro

N = 512                     # 训练序列长度/载波数,满足：L<=N
P = 36                      # 导频数，P<N

''' 非法用户猜测导频位置，猜对数的概率 '''
pro,maxright = eva_guess_pro(N,P)
print ('Most probabily guess right:Pro(%d)=%f'%(maxright,pro[maxright]))

plt.figure(figsize=(8,5))
plt.plot(pro,'bo-')
plt.plot(maxright,pro[maxright],'ro')
plt.xlabel('number of right pilots')
plt.ylabel('probability')
plt.title('Probability of the number of right pilots')