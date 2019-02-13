#encoding=utf-8
###############
# 基于EditDistance模型计算表情的相似度
##################
from json import dumps
from config import connect_db
from tools.similar.edit_distance import ed_max_similar, edit_distance
from time import time


def tag_edit_distance(analysis_nids=[], tag_table='novel_base_tag', out_table='similar_base_tag', debug=False, save_limit=None):
    con = connect_db()
    cur = con.cursor()
    letter_group = []
    word_group = []
    nids = []
    vals = []
    analysis_nids = [str(nid[0]) for nid in analysis_nids]
    tstart = time()
    cur.execute(
        "SELECT nid, group_concat(tag) as tags FROM (SELECT * FROM `" + tag_table + "` WHERE nid in (" + ','.join(
            analysis_nids) + ")) t GROUP BY nid")
    ret = cur.fetchall()
    for item in ret:
        nids.append(item[0])
        letter_group.append(item[1].replace(',', ''))
        word_group.append(item[1].split(','))
    if len(nids) < len(analysis_nids):
        print '以下小说编号未录入数据库：', set(analysis_nids).difference(set(nids))
    print '导入数据耗时：', time()-tstart
    tstart = time()
    for i in range(0, len(letter_group)):
        for j in range(i + 1, len(letter_group)):
            letter_similar = edit_distance(letter_group[i], letter_group[j], debug=debug)
            word_max_similar = ed_max_similar(word_group[i], word_group[j], debug=debug)
            total_similar = word_max_similar * letter_similar
            vals.append((nids[i], nids[j], word_max_similar, letter_similar, total_similar))
            if debug:
                print dumps(word_group[i], ensure_ascii=False)
                print dumps(word_group[j], ensure_ascii=False)
                print letter_similar, word_max_similar, total_similar
                print '-----'
        if save_limit is not None:
            vals = sorted(vals, key=lambda x: x[4], reverse=True)[:save_limit]
        cur.executemany("INSERT INTO `" + out_table + "` (`nid1`, `nid2`, `type`, `word`, `letter`, `total`) VALUES (%s, %s, 'edit_distance', %s, %s, %s)", vals)
        con.commit()
        vals = []
    print '分析结束，耗时：', time()-tstart
    cur.close()
    con.close()


if __name__ == '__main__':

    # ret = [['100089917'], ['100055607'], ['100089784'], ['100060280'],
    #        ['100087736'], ['100077651'], ['100025807'], ['100084396'],
    #        ['100000514'], ['100079016'], ['100072902'], ['100070345'],
    #        ['100003883'], ['100057499'], ['100028599'], ['100000748'],
    #        ['100061867'], ['100061338'], ['100056917'], ['100011818'],
    #        ['100049348'], ['100056938'], ['100035330'], ['100045203'],
    #        ['100042006']]

    # ret = [['100049348'], ['100061338']]

    con = connect_db()
    cur = con.cursor()
    # cur.execute("SELECT nid FROM `fan_shelf` ORDER BY collect DESC Limit 5")
    cur.execute("SELECT `nid` FROM `novel_info` AS a LEFT JOIN (SELECT DISTINCT `nid1` as `nnid` FROM `similar_base_tag`) AS b ON a.nid = b.nnid WHERE b.nnid IS NULL")
    ret = cur.fetchall()
    cur.close()
    con.close()

    debug = False
    tag_edit_distance(ret, debug=debug)
    tag_edit_distance(ret, tag_table='novel_description_tag', out_table='similar_description_tag', debug=debug)
