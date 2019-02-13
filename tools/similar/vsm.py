#encoding=utf-8
################
# VSM 余弦词向量模型计算标签相似度
# 参考：https://blog.csdn.net/u010598982/article/details/50985994
#      http://www.ruanyifeng.com/blog/2013/03/cosine_similarity.html
###############
from math import sqrt
from json import dumps


# 合并标签集
def create_vocabulary(tag_list1, tag_list2):
    return list(set(tag_list1+tag_list2))


# 统计词频
def calc_tag_frequency(tag_list):
    tag_frequency = {}
    tag_set = set(tag_list)
    for tag in tag_set:
        tag_frequency[tag] = tag_list.count(tag)
    return tag_frequency


# 建立词频向量
def create_vector(tag_frequency, vocabulary):
    vector = []
    tag_set = tag_frequency.keys()
    for tag in vocabulary:
        if tag in tag_set:
            vector.append(tag_frequency[tag])
        else:
            vector.append(0)
    return vector


# 计算词频向量相似度
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


def vsm(tag_list1, tag_list2, debug=False):
    count = len(tag_list1) + len(tag_list2)
    vocabulary = create_vocabulary(tag_list1, tag_list2)
    vector1 = create_vector(calc_tag_frequency(tag_list1), vocabulary)
    vector2 = create_vector(calc_tag_frequency(tag_list2), vocabulary)
    similar = calc_similar(vector1, vector2, count)
    if debug:
        print 'vocabulary', dumps(vocabulary, ensure_ascii=False)
        print 'vector1', vector1
        print 'vector2', vector2
        print 'similar', similar
    return similar
