# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 00:02:45 2016

@author: gymmer
"""

import numpy as np
from numpy import array,pi

def grayCode_4bit(value):
    if value>=0 and value<pi/8:
        return array([0,0,0,0])
    if value>=pi/8 and value<2*pi/8:
        return array([0,0,0,1])
    if value>=2*pi/8 and value<3*pi/8:
        return array([0,0,1,1])
    if value>=3*pi/8 and value<4*pi/8:
        return array([0,0,1,0])
    if value>=4*pi/8 and value<5*pi/8:
        return array([0,1,1,0])
    if value>=5*pi/8 and value<6*pi/8:
        return array([0,1,1,1])
    if value>=6*pi/8 and value<7*pi/8:
        return array([0,1,0,1])
    if value>=7*pi/8 and value<8*pi/8:
        return array([0,1,0,0])
    if value>=8*pi/8 and value<9*pi/8:
        return array([1,1,0,0])
    if value>=9*pi/8 and value<10*pi/8:
        return array([1,1,0,1])
    if value>=10*pi/8 and value<11*pi/8:
        return array([1,1,1,1])
    if value>=11*pi/8 and value<12*pi/8:
        return array([1,1,1,0])
    if value>=12*pi/8 and value<13*pi/8:
        return array([1,0,1,0])
    if value>=13*pi/8 and value<14*pi/8:
        return array([1,0,1,1])
    if value>=14*pi/8 and value<15*pi/8:
        return array([1,0,0,1])
    if value>=15*pi/8 and value<2*pi:
        return array([1,0,0,0])

def naturalCode_4bit(value):
    if value>=0 and value<pi/8:
        return array([0,0,0,0])
    if value>=pi/8 and value<2*pi/8:
        return array([0,0,0,1])
    if value>=2*pi/8 and value<3*pi/8:
        return array([0,0,1,0])
    if value>=3*pi/8 and value<4*pi/8:
        return array([0,0,1,1])
    if value>=4*pi/8 and value<5*pi/8:
        return array([0,1,0,0])
    if value>=5*pi/8 and value<6*pi/8:
        return array([0,1,0,1])
    if value>=6*pi/8 and value<7*pi/8:
        return array([0,1,1,0])
    if value>=7*pi/8 and value<8*pi/8:
        return array([0,1,1,1])
    if value>=8*pi/8 and value<9*pi/8:
        return array([1,0,0,0])
    if value>=9*pi/8 and value<10*pi/8:
        return array([1,0,0,1])
    if value>=10*pi/8 and value<11*pi/8:
        return array([1,0,1,0])
    if value>=11*pi/8 and value<12*pi/8:
        return array([1,0,1,1])
    if value>=12*pi/8 and value<13*pi/8:
        return array([1,1,0,0])
    if value>=13*pi/8 and value<14*pi/8:
        return array([1,1,0,1])
    if value>=14*pi/8 and value<15*pi/8:
        return array([1,1,1,0])
    if value>=15*pi/8 and value<2*pi:
        return array([1,1,1,1])
        
def grayCode_3bit(value):
    if value>=0 and value<pi/4:
        return array([0,0,0])
    if value>=pi/4 and value<2*pi/4:
        return array([0,0,1])
    if value>=2*pi/4 and value<3*pi/4:
        return array([0,1,1])
    if value>=3*pi/4 and value<4*pi/4:
        return array([0,1,0])
    if value>=4*pi/4 and value<5*pi/4:
        return array([1,1,0])
    if value>=5*pi/4 and value<6*pi/4:
        return array([1,1,1])
    if value>=6*pi/4 and value<7*pi/4:
        return array([1,0,1])
    if value>=7*pi/4 and value<2*pi:
        return array([1,0,0])

def naturalCode_3bit(value):
    if value>=0 and value<pi/4:
        return array([0,0,0])
    if value>=pi/4 and value<2*pi/4:
        return array([0,0,1])
    if value>=2*pi/4 and value<3*pi/4:
        return array([0,1,0])
    if value>=3*pi/4 and value<4*pi/4:
        return array([0,1,1])
    if value>=4*pi/4 and value<5*pi/4:
        return array([1,0,0])
    if value>=5*pi/4 and value<6*pi/4:
        return array([1,0,1])
    if value>=6*pi/4 and value<7*pi/4:
        return array([1,1,0])
    if value>=7*pi/4 and value<2*pi:
        return array([1,1,1])
        
def grayCode_2bit(value):
    if value>=0 and value<pi/2:
        return array([0,0])
    if value>=pi/2 and value<pi:
        return array([0,1])
    if value>=pi and value<3*pi/2:
        return array([1,1])
    if value>=3*pi/2 and value<2*pi:
        return array([1,0])

def naturalCode_2bit(value):
    if value>=0 and value<pi/2:
        return array([0,0])
    if value>=pi/2 and value<pi:
        return array([0,1])
    if value>=pi and value<3*pi/2:
        return array([1,0])
    if value>=3*pi/2 and value<2*pi:
        return array([1,1])

def Code_1bit(value):
    if value>=0 and value<pi:
        return array([0])
    if value>=pi and value<2*pi:
        return array([1]) 