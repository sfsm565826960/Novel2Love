#encoding=utf-8
#################
# Edit Distance 标签编辑次数距离相似度算法
# 参考：https://www.cnblogs.com/jingsupo/p/python-Levenshtein.html
#################


def edit_distance(vtag, htag, debug=False):
    vtag = list(vtag)
    htag = list(htag)
    vlen = len(vtag) + 1
    hlen = len(htag) + 1
    if vlen == 1 or hlen == 1:  # 若其中一个标签为空，则直接返回相似度为0
        return 0
    dic = [[i for i in range(hlen)]]
    for v in range(1, vlen):
        dic.append([0] * hlen)
        dic[v][0] = v
    for v in range(1, vlen):
        for h in range(1, hlen):
            val = 0 if vtag[v - 1] == htag[h - 1] else 1
            dic[v][h] = min(dic[v - 1][h - 1] + val, dic[v][h - 1] + 1, dic[v - 1][h] + 1)
    similarity = 1 - dic[vlen - 1][hlen - 1] / float(max(vlen - 1, hlen - 1))
    return similarity


def ed_max_similar(tags1, tags2, debug=False):
    similar = []
    min_tags = tags1
    max_tags = tags2
    if len(tags1) > len(tags2):
        min_tags = tags2
        max_tags = tags1
    for t1 in min_tags:
        ed = []
        for t2 in max_tags:
            ed.append(edit_distance(t1, t2))
        similar.append(max(ed))
    if debug:
        print similar
    return sum(similar)
