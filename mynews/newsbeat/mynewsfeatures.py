# -*- coding: utf-8 -*-
"""
搜集新闻源，并将各文章里出现的词转换成数字矩阵
"""
import os
import re
import feedparser
import jieba
import numpy as np


PUNCT = set(u''':!),.:;?>]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
﹔﹕﹖﹗﹚﹜﹞！）/<$&#@，．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

FEEDLIST = [
    'http://news.qq.com/newsgn/rss_newsgn.xml',
    'http://news.baidu.com/n?cmd=4&class=civilnews&tn=rss',
    'http://news.baidu.com/n?cmd=4&class=internews&tn=rss',
    'http://www.xinhuanet.com/politics/news_politics.xml',
    'http://www.xinhuanet.com/world/news_world.xml',
    'http://www.people.com.cn/rss/politics.xml',
    'http://www.people.com.cn/rss/world.xml',
    'http://news.163.com/special/00011K6L/rss_newsattitude.xml'
]

STOP_WORDS_FILE = os.path.join(os.path.dirname(__file__), 'stop_words.txt')
STOP_WORDS = {line.strip() for line in open(STOP_WORDS_FILE, encoding='utf-8').readlines()}

# TFIDF
# jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
# jieba.analyse.set_stop_words(file_name) # file_name为自定义语料库的路径

def separatewords(text):
    """分词"""
    seg_list = jieba.cut(text)
    return (word.lower() for word in seg_list if word not in STOP_WORDS)


def getarticlewords():
    """获取词频"""
    allwords = {}  # 记录单词在所有文章中被使用的次数
    articlewords = []  # 单词在每篇文章中出现的次数
    articletitles = []  # 文章标题列表
    entrycount = 0
    # 遍历每个订阅源
    for url in FEEDLIST:
        feed = feedparser.parse(url)
        # 遍历每篇文章
        for entry in feed.entries:
            # 跳过标题相同的文章
            if entry.title in articletitles:
                continue
            # 提取单词
            text = entry.title + entry.description
            text = re.compile(r'<[^>]+>').sub(' ', text)  # 去除html标记
            words = separatewords(text)
            articlewords.append({})
            articletitles.append(entry.title)
            # 在allwords和articlewords中增加对当前单词的计数
            for word in words:
                allwords.setdefault(word, 0)
                allwords[word] += 1
                articlewords[entrycount].setdefault(word, 0)
                articlewords[entrycount][word] += 1
            entrycount += 1

    return allwords, articlewords, articletitles


def makematrix(allwords, articlewords, common_rate=0.6):
    """只考虑在超过三篇文章中出现过
    且在所有文章中出现的比例小于60%的词
    """
    # 只考虑那些普通的但又不至于非常普通的词
    wordvec = []
    for word, count in allwords.items():
        if count > 3 and count < len(articlewords) * common_rate:
            wordvec.append(word)
    # 构造单词矩阵
    word_matrix = [[(word in article and article[word] or 0)
                    for word in wordvec]
                   for article in articlewords]
    # word in article --->True or False
    # True/False and article[word]--->False or article[word]
    return word_matrix, wordvec


def showfeatures(weight, feature, titles, wordvec, out='myfeatures.txt'):
    """显示特征"""
    outfile = open(out, 'w', encoding='utf8')
    pc, wc = np.shape(feature)  # pc 特征数，wc 词向量维数
    toppatterns = [[] for i in range(len(titles))]
    patternnames = []

    # 遍历所有特征
    for i in range(pc):
        slist = []
        # 构造一个包含单词及其权重数据的列表
        for j in range(wc):
            slist.append((feature[i, j], wordvec[j]))
        # 将单词列表倒序排列
        slist.sort(reverse=True)

        # 打印权重最高的6个词
        topwords_num = 6
        words = [s[1] for s in slist[:topwords_num]]
        outfile.write(str(words) + '\n')
        patternnames.append(words)

        # 构造一个针对该特征的文章列表
        flist = []
        for j, title in enumerate(titles):
            # 加入文章及其权重数据
            flist.append((weight[j, i], title))
            toppatterns[j].append((weight[j, i], i, title))

        # Reverse sort the list
        flist.sort(reverse=True)

        # Show the top 5 articles
        toparticle_num = 5
        for article in flist[:toparticle_num]:
            outfile.write(str(article) + '\n')
        outfile.write('\n')

    outfile.close()
    # Return the pattern names for later use
    return toppatterns, patternnames


def showarticles(titles, toppatterns, patternnames, out='myarticles.txt'):
    """display by articles"""
    outfile = open(out, 'w', encoding='utf8')
    # 遍历所有文章
    for j, title in enumerate(titles):
        outfile.write(title)
        outfile.write('\n')
        # 针对该篇文章, 获得排位最靠前的几个特征
        toppatterns[j].sort(reverse=True)
        # 打印前5个特征
        topp_num = 5
        for i in range(topp_num):
            outfile.write(str(toppatterns[j][i][0]) + ' ' +
                          str(patternnames[toppatterns[j][i][1]]) + '\n')
        outfile.write('\n')
    outfile.close()


def get_features1(weight, feature, titles, wordvec):
    """显示特征"""
    out = []  # 返回结果
    pc, wc = np.shape(feature)  # pc 特征数，wc 词向量维数
    toppatterns = [[] for i in range(len(titles))]
    patternnames = []

    # 遍历所有特征
    for i in range(pc):
        out.append({})  # 每个topic一个结果字典
        out[i]['id'] = i #每个结果的id

        slist = []
        # 构造一个包含单词及其权重数据的列表
        for j in range(wc):
            slist.append((feature[i, j], wordvec[j]))
        # 将单词列表倒序排列
        slist.sort(reverse=True)

        # 打印权重最高的6个词
        topwords_num = 6
        words = [s[1] for s in slist[:topwords_num]]
        feature_words = ','.join(words)
        out[i]['feature'] = feature_words

        patternnames.append(words)

        # 构造一个针对该特征的文章列表
        flist = []
        for j, title in enumerate(titles):
            # 加入文章及其权重数据
            flist.append((weight[j, i], title))
            toppatterns[j].append((weight[j, i], i, title))

        # Reverse sort the list
        flist.sort(reverse=True)

        # Show the top 5 articles
        toparticle_num = 5
        articles = []
        for article in flist[:toparticle_num]:
            articles.append('{}: {}'.format(*article))
        out[i]['related_articles'] = articles
    # Return the pattern names for later use
    return out

def get_features(weight, feature, titles, wordvec):
    """返回json字典给django -html"""
    # out = {}  # 返回结果
    out = {}
    out_str = []
    pc, wc = np.shape(feature)  # pc 特征数，wc 词向量维数
    toppatterns = [[] for i in range(len(titles))]
    patternnames = []

    # 遍历所有特征
    for i in range(pc):
        # out.append({})  # 每个topic一个结果字典
        # out[i]['id'] = i #每个结果的id

        slist = []
        # 构造一个包含单词及其权重数据的列表
        for j in range(wc):
            slist.append((feature[i, j], wordvec[j]))
        # 将单词列表倒序排列
        slist.sort(reverse=True)

        # 打印权重最高的10个词
        topwords_num = 10
        words = [s[1].encode('utf-8').decode() for s in slist[:topwords_num]]
        feature_words = ','.join(words)
        index = str(i)
        out[index] = {}
        out[index]['feature'] = feature_words
        

        patternnames.append(words)

        # 构造一个针对该特征的文章列表
        flist = []
        for j, title in enumerate(titles):
            # 加入文章及其权重数据
            flist.append((weight[j, i], title))
            toppatterns[j].append((weight[j, i], i, title))

        # Reverse sort the list
        flist.sort(reverse=True)

        # Show the top 5 articles
        toparticle_num = 5
        articles = {}
        for num, article in enumerate(flist[:toparticle_num], start=1):
            key = str(num)
            articles[key] = '{}: {}'.format(str(article[0]),
                                            article[1].encode('utf-8').decode('utf-8'))
        out[index]['related_articles'] = articles
        #out[feature_words] = articles
        #topic_sum = '<br/ >'.join((feature_words, *articles.values()))
        #out_str.append(topic_sum)
    
    # Return the pattern names for later use
    # return '<br/ ><br />'.join(out_str)
    return out