# -*- coding: utf-8 -*-

'''
OFDM communication default parameters
'''

dL   = 50      		# 信道长度
dK   = 6        		# 稀疏度/多径数，满足:K<<L
dN   = 512      		# 训练序列长度/载波数,满足：L<=N
dNcp = 60       		# 循环前缀长度,Ncp>L
dmodulate = 4   		# 星座调制: 1 -> BPSK,  2 -> QPSK,  4 -> 16QAM
dSNR = 20             # AWGN信道信噪比
detype    = "CS"		# 信道估计类型。'CS' 或 'LS'
dpos_type = "from_pos"# 'from_pos'：使用传入的参数 pos 作为导频图样
        				# 其他（数字类型）：与 pos 相比，猜对了其中【数字】个导频位置