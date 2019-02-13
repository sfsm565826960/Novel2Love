#encoding=utf-8
################
# VSM 余弦词向量模型计算标签相似度
# 参考：https://blog.csdn.net/u010598982/article/details/50985994
#      http://www.ruanyifeng.com/blog/2013/03/cosine_similarity.html
###############
from math import sqrt
from json import dumps


def create_vocabulary(tag_group1, tag_group2):
    return list(set(tag_group1+tag_group2))


def calc_vector(tag_group, vocabulary):
    vector = []
    for tag in vocabulary:
        if tag in tag_group:
            vector.append(1)
        else:
            vector.append(0)
    return vector


def calc_similar(vector1, vector2, tag_count):
    x = 0.0 # 分子
    y1 = 0.0 # 分母1
    y2 = 0.0 # 分母2
    tag_count = float(tag_count)
    for i in range(0, len(vector1)): # same length
        t1 = vector1[i] / tag_count
        t2 = vector2[i] / tag_count
        x = x + (t1 * t2)
        y1 += pow(t1, 2)
        y2 += pow(t2, 2)
    return x / sqrt(y1 * y2)


def vsm(tag_group1, tag_group2, debug=False):
    count = len(tag_group1) + len(tag_group2)
    vocabulary = create_vocabulary(tag_group1, tag_group2)
    vector1 = calc_vector(tag_group1, vocabulary)
    vector2 = calc_vector(tag_group2, vocabulary)
    similar = calc_similar(vector1, vector2, count)
    if debug:
        print 'vocabulary', dumps(vocabulary, ensure_ascii=False)
        print 'vector1', vector1
        print 'vector2', vector2
        print 'similar', similar
    return similar
