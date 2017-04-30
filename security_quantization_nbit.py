# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 00:02:45 2016

@author: gymmer
"""

from numpy import array

def grayCode_4bit(minimum,interval,value):
    if value>=minimum+0*interval and value<minimum+1*interval:
        return array([0,0,0,0])
    if value>=minimum+1*interval and value<minimum+2*interval:
        return array([0,0,0,1])
    if value>=minimum+2*interval and value<minimum+3*interval:
        return array([0,0,1,1])
    if value>=minimum+3*interval and value<minimum+4*interval:
        return array([0,0,1,0])
    if value>=minimum+4*interval and value<minimum+5*interval:
        return array([0,1,1,0])
    if value>=minimum+5*interval and value<minimum+6*interval:
        return array([0,1,1,1])
    if value>=minimum+6*interval and value<minimum+7*interval:
        return array([0,1,0,1])
    if value>=minimum+7*interval and value<minimum+8*interval:
        return array([0,1,0,0])
    if value>=minimum+8*interval and value<minimum+9*interval:
        return array([1,1,0,0])
    if value>=minimum+9*interval and value<minimum+10*interval:
        return array([1,1,0,1])
    if value>=minimum+10*interval and value<minimum+11*interval:
        return array([1,1,1,1])
    if value>=minimum+11*interval and value<minimum+12*interval:
        return array([1,1,1,0])
    if value>=minimum+12*interval and value<minimum+13*interval:
        return array([1,0,1,0])
    if value>=minimum+13*interval and value<minimum+14*interval:
        return array([1,0,1,1])
    if value>=minimum+14*interval and value<minimum+15*interval:
        return array([1,0,0,1])
    if value>=minimum+15*interval and value<=minimum+16*interval:
        return array([1,0,0,0])

def naturalCode_4bit(minimum,interval,value):
    if value>=minimum+0*interval and value<minimum+1*interval:
        return array([0,0,0,0])
    if value>=minimum+1*interval and value<minimum+2*interval:
        return array([0,0,0,1])
    if value>=minimum+2*interval and value<minimum+3*interval:
        return array([0,0,1,0])
    if value>=minimum+3*interval and value<minimum+4*interval:
        return array([0,0,1,1])
    if value>=minimum+4*interval and value<minimum+5*interval:
        return array([0,1,0,0])
    if value>=minimum+5*interval and value<minimum+6*interval:
        return array([0,1,0,1])
    if value>=minimum+6*interval and value<minimum+7*interval:
        return array([0,1,1,0])
    if value>=minimum+7*interval and value<minimum+8*interval:
        return array([0,1,1,1])
    if value>=minimum+8*interval and value<minimum+9*interval:
        return array([1,0,0,0])
    if value>=minimum+9*interval and value<minimum+10*interval:
        return array([1,0,0,1])
    if value>=minimum+10*interval and value<minimum+11*interval:
        return array([1,0,1,0])
    if value>=minimum+11*interval and value<minimum+12*interval:
        return array([1,0,1,1])
    if value>=minimum+12*interval and value<minimum+13*interval:
        return array([1,1,0,0])
    if value>=minimum+13*interval and value<minimum+14*interval:
        return array([1,1,0,1])
    if value>=minimum+14*interval and value<minimum+15*interval:
        return array([1,1,1,0])
    if value>=minimum+15*interval and value<=minimum+16*interval:
        return array([1,1,1,1])
        
def grayCode_3bit(minimum,interval,value):
    if value>=minimum+0*interval and value<minimum+1*interval:
        return array([0,0,0])
    if value>=minimum+1*interval and value<minimum+2*interval:
        return array([0,0,1])
    if value>=minimum+2*interval and value<minimum+3*interval:
        return array([0,1,1])
    if value>=minimum+3*interval and value<minimum+4*interval:
        return array([0,1,0])
    if value>=minimum+4*interval and value<minimum+5*interval:
        return array([1,1,0])
    if value>=minimum+5*interval and value<minimum+6*interval:
        return array([1,1,1])
    if value>=minimum+6*interval and value<minimum+7*interval:
        return array([1,0,1])
    if value>=minimum+7*interval and value<=minimum+8*interval:
        return array([1,0,0])

def naturalCode_3bit(minimum,interval,value):
    if value>=minimum+0*interval and value<minimum+1*interval:
        return array([0,0,0])
    if value>=minimum+1*interval and value<minimum+2*interval:
        return array([0,0,1])
    if value>=minimum+2*interval and value<minimum+3*interval:
        return array([0,1,0])
    if value>=minimum+3*interval and value<minimum+4*interval:
        return array([0,1,1])
    if value>=minimum+4*interval and value<minimum+5*interval:
        return array([1,0,0])
    if value>=minimum+5*interval and value<minimum+6*interval:
        return array([1,0,1])
    if value>=minimum+6*interval and value<minimum+7*interval:
        return array([1,1,0])
    if value>=minimum+7*interval and value<=minimum+8*interval:
        return array([1,1,1])
        
def grayCode_2bit(minimum,interval,value):
    if value>=minimum+0*interval and value<minimum+1*interval:
        return array([0,0])
    if value>=minimum+1*interval and value<minimum+2*interval:
        return array([0,1])
    if value>=minimum+2*interval and value<minimum+3*interval:
        return array([1,1])
    if value>=minimum+3*interval and value<=minimum+4*interval:
        return array([1,0])

def naturalCode_2bit(minimum,interval,value):
    if value>=minimum+0*interval and value<minimum+1*interval:
        return array([0,0])
    if value>=minimum+1*interval and value<minimum+2*interval:
        return array([0,1])
    if value>=minimum+2*interval and value<minimum+3*interval:
        return array([1,0])
    if value>=minimum+3*interval and value<=minimum+4*interval:
        return array([1,1])

def Code_1bit(minimum,interval,value):
    if value>=minimum+0*interval and value<minimum+1*interval:
        return array([0])
    if value>=minimum+1*interval and value<=minimum+2*interval:
        return array([1]) 