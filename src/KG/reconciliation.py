# -*- coding: utf-8 -*-

from cascade import cascade
from winnow import winnow

def reconciliation(bits_A,bits_B,rtype,iteration):
    '''
    bits_A: Alice的二进制序列
    bits_B: Bob的二进制序列
    rtype: 信息协调方式。cascade/winnow
    iteration: 信息协调迭代次数
    '''
    if rtype == 'cascade':
        return cascade(bits_A,bits_B,iteration)
    elif rtype == 'winnow':
        return winnow(bits_A,bits_B,iteration)