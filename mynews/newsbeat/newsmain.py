# -*- coding: utf-8 -*-

from newsbeat.mynewsfeatures import getarticlewords, makematrix, showarticles, showfeatures, get_features
from newsbeat import mynnmf
import numpy as np


def run():
    # all_words: 记录单词在所有文章中被使用的次数(字典)
    # article_words: 单词在每篇文章中出现的次数(包含字典的列表)
    # article_titles: 文章标题列表
    all_words, article_words, article_titles = getarticlewords()
    # word_matrix:构造word_vec中单词在每篇文中出现次数的矩阵
    # word_vec: 非普遍词的列表
    word_matrix, word_vec = makematrix(all_words, article_words)

    # news_matrics
    news_matrics = np.matrix(word_matrix) # 矩阵化
    w, h = mynnmf.factorize(news_matrics, k=10, maxiter=20) # k是期望特征数

    #top_patterns, pattern_names = showfeatures(w, h, article_titles, word_vec, out='myfeatures.txt')
    result = get_features(w, h, article_titles, word_vec)
    return result
    # showarticles(article_titles, top_patterns, pattern_names, out='myarticles.txt')



