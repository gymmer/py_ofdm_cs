# -*- coding: utf-8 -*-

import sys
import numpy as np
from numpy import array

sys.path.append('../')
from util.from_to import from2seq_to10

def encode(bits,P,exclude=[]):
    '''
    从二进制流中，编码得到P个不重复的导频位置
    bits: 二进制流
    P: 导频数量
    exclude: 导频位置不与exclude中的位置重复
    返回值: 导频图样
    '''

    pos = array([],dtype=np.int32)          # 初始化导频图样pos为空
    pos_num = 0                             # 已生成的导频数。初始时未生成导频，为0
    index = 0
    while(pos_num<P):                       # 循环停止的条件是，已经根据密钥流产生了足够数量的导频位置
        seed = bits[index*9:(index+1)*9]    # 如果N=512,则导频位置的取值范围[0,512]，需要对9位二进制转成十进制。
        index += 1
        new_pos = int(from2seq_to10(seed))  # 密钥流每读入9个比特，则计算一次新产生的导频位置
        if new_pos not in pos and new_pos not in exclude:              # 如果新增导频不在我的已有导频列表中，则加入这个导频
            pos = np.r_[pos,new_pos]        # 如果已有导频列表中已有该导频，则放弃。防止重复加入多个相同的同频位置
            pos_num += 1                    # 修改已产生的导频位置数
    return pos