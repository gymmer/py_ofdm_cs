# -*- coding: utf-8 -*-

'''
MIMO communication default parameters
'''

dL   = 50      	     # 信道长度
dK   = 6        		# 稀疏度/多径数，满足:K<<L
dN   = 512      		# 训练序列长度/载波数,满足：L<=N
dNcp = 60       		# 循环前缀长度,Ncp>L
dM   = 8              # 每帧的OFDM符号数
dNt  = 2              # 发送天线数
dNr  = 1              # 接收天线数 
dSNR = 20             # AWGN信道信噪比
dmodulate = 4   		# 星座调制: 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
detype    = "CS"		# 信道估计类型。'CS' 或 'LS'