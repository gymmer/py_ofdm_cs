# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 00:03:32 2016

@author: gymmer
"""

import numpy as np
from numpy import pi

def sampling(N):
    return 2*pi*np.random.random(N)     # [0,2pi)之间均匀分布