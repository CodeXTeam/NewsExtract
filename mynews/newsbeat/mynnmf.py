# -*- coding: utf-8 -*-
"""
NMF:非负矩阵因式分解
"""
import random
import numpy as np


def difcost(matrixa, matrixb):
    """
    计算构造矩阵与原矩阵的接近程度
    矩阵中每个值的差值的平方和
    """
    cost = 0
    # 遍历矩阵
    for i in range(np.shape(matrixa)[0]):
        for j in range(np.shape(matrixa)[1]):
            # 将差值平方相加
            cost += pow(matrixa[i, j] - matrixb[i, j], 2)
    return cost


def factorize(vec, k=10, maxiter=50):
    """
    vec是数据矩阵(m x n 维)，k是期望特征数，maxiter是最大迭代次数
    乘法更新法则，产生4个新的更新矩阵
    """
    # 以随机值初始化权重矩阵W(m x k 维)和特征矩阵H(k x n 维)
    m = np.shape(vec)[0]  # 数据矩阵vec行数
    n = np.shape(vec)[1]  # 数据矩阵vec列数
    W = np.matrix([[random.random()
                    for j in range(k)]
                   for i in range(m)])  # (m, k)维
    H = np.matrix([[random.random()
                    for j in range(n)]
                   for i in range(k)])  # (k, n)维

    # 迭代更新矩阵
    for i in range(maxiter):
        WH = W * H
        # 计算当前值
        cost = difcost(vec, WH)
        if i % 10 == 0:
            print("cost after %d iterations:%f" % (i, cost))
        # 如果矩阵分解彻底，则终止
        if cost == 0:
            break
        # 更新特征矩阵
        Hn = (np.transpose(W) * vec)  # (k, n) 维
        Hd = (np.transpose(W) * W * H)  # (k, n) 维
        H = np.matrix(np.array(H) * np.array(Hn) / np.array(Hd))
        # 更新权重矩阵
        Wn = (vec * np.transpose(H))  # (m, k)
        Wd = (W * H * np.transpose(H))  # (m, k)
        W = np.matrix(np.array(W) * np.array(Wn) / np.array(Wd))

    return W, H



