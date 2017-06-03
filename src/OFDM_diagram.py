# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 20:56:31 2016

@author: My402
"""
import numpy as np
from numpy import array,sqrt
from from_to import from2seq_to10

''' 星座点的归一化系数 '''
normal_coef = {
    1:sqrt(1),
    2:sqrt(2),
    4:sqrt(10)}
    
''' 星座映射的格雷码'''
BPSK_list  = [-1+0j,+1+0j]
QPSK_list  = [-1-1j,-1+1j,+1-1j,+1+1j]
QAM16_list = [-3-3j,-3-1j,-3+3j,-3+1j,-1-3j,-1-1j,-1+3j,-1+1j,
              +3-3j,+3-1j,+3+3j,+3+1j,+1-3j,+1-1j,+1+3j,+1+1j]

BPSK_dict = {
    -1+0j:array([0]),+1+0j:array([1])}

QPSK_dict = {
    -1-1j:array([0,0]),-1+1j:array([0,1]),
    +1-1j:array([1,0]),+1+1j:array([1,1])}
    
QAM16_dict = {
    -3-3j:array([0,0,0,0]),-3-1j:array([0,0,0,1]),
    -3+3j:array([0,0,1,0]),-3+1j:array([0,0,1,1]),
    -1-3j:array([0,1,0,0]),-1-1j:array([0,1,0,1]),
    -1+3j:array([0,1,1,0]),-1+1j:array([0,1,1,1]),
    +3-3j:array([1,0,0,0]),+3-1j:array([1,0,0,1]),
    +3+3j:array([1,0,1,0]),+3+1j:array([1,0,1,1]),
    +1-3j:array([1,1,0,0]),+1-1j:array([1,1,0,1]),
    +1+3j:array([1,1,1,0]),+1+1j:array([1,1,1,1])}

def BPSK_mod(bits):
    return BPSK_list[ from2seq_to10(bits) ]
    
def QPSK_mod(bits):
    return QPSK_list[ from2seq_to10(bits) ]
    
def QAM16_mod(bits):
    return QAM16_list[ from2seq_to10(bits) ]

def BPSK_demod(symbol):
    if symbol.real<=0:
        rp = -1
    else:
        rp = 1
    ip = 0
    return BPSK_dict[rp+1j*ip]
        
def QPSK_demod(symbol):
    if symbol.real<=0:
        rp = -1
    else:
        rp = 1
        
    if symbol.imag<=0:
        ip = -1
    else:
        ip = 1
    return QPSK_dict[rp+1j*ip]

def QAM16_demod(symbol):
    if symbol.real<=-2:
        rp = -3
    elif symbol.real>-2 and symbol.real<=0:
        rp = -1
    elif symbol.real>0  and symbol.real<2:
        rp = 1
    else:
        rp = 3
        
    if symbol.imag<=-2:
        ip = -3
    elif symbol.imag>-2 and symbol.imag<=0:
        ip = -1
    elif symbol.imag>0  and symbol.imag<2:
        ip = 1
    else:
        ip = 3
    return QAM16_dict[rp+1j*ip]
    
def diagram_mod(bits,modulate_type):
    '''
    bits: 待调制的输入比特流
    modulate_type: 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
    '''

    # 对于16QAM，每4个bit编码产生一个星座点。
    # 同理，BPSK为1个bit产生一个星座点，QPSK为2个bit
    # 因此，将输入的比特流，划分成M组
    M = bits.size/modulate_type
    bits = np.array_split(bits, M)
    
    # 对每组的1个/2个/4个bit做星座点映射
    if modulate_type==1:
        diagram = [ BPSK_mod(x) for x in bits ]
    elif modulate_type==2:
        diagram = [ QPSK_mod(x) for x in bits ]
    elif modulate_type==4:
        diagram = [ QAM16_mod(x) for x in bits ]
    diagram = np.hstack(diagram)
    return diagram

def diagram_demod(diagram,demodulate_type):
    '''
    diagram: 待解调的星座点序列
    modulate_type: 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
    '''
    M = diagram.size
    diagram = np.array_split(diagram, M)
    if demodulate_type==1:
        bits = [ BPSK_demod(x) for x in diagram ]
    elif demodulate_type==2:
        bits = [ QPSK_demod(x) for x in diagram ]
    elif demodulate_type==4:
        bits = [ QAM16_demod(x) for x in diagram ]
    bits = np.hstack(bits)
    return bits