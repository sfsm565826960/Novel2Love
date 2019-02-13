#encoding=utf-8
################
# VSM结合EditDistance模型计算标签相似度
###############
from vsm import create_vocabulary, calc_similar
from edit_distance import edit_distance
from json import dumps


def calc_edit_distance_vector(tag_group, vocabulary, debug=False):
    vector = []
    for tag1 in vocabulary:
        if len(tag1) == 1:
            vector.append(1 if tag1 in tag_group else 0)
        else:
            similar = []
            for tag2 in tag_group:
                similar.append(edit_distance(tag1, tag2, debug))
            vector.append(max(similar))
            if debug:
                print 'calc_edit_distance_vector', tag1, dumps(vocabulary, ensure_ascii=False), similar
    return vector


def edit_distance_vsm(tag_group1, tag_group2, debug=False):
    count = len(tag_group1) + len(tag_group2)
    vocabulary = create_vocabulary(tag_group1, tag_group2)
    vector1 = calc_edit_distance_vector(tag_group1, vocabulary, debug)
    vector2 = calc_edit_distance_vector(tag_group2, vocabulary, debug)
    similar = calc_similar(vector1, vector2, count)
    if debug:
        print 'vocabulary', dumps(vocabulary, ensure_ascii=False)
        print 'vector1', vector1
        print 'vector2', vector2
        print 'similar', similar
        print '-------'
    return similar
