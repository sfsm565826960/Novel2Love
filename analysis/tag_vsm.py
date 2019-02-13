#encoding=utf-8
#################
# 基于VSM进行标签分析，获取最相似的前N个小说
################
from json import dumps
from config import connect_db
from tools.similar.vsm import vsm
from time import time


def import_tag_data(cur, table, nids):
    t_nids = []
    word_group = []
    letter_group = []
    cur.execute("SELECT nid, group_concat(tag) as tags FROM (SELECT * FROM `" + table + "` WHERE nid in (" + ','.join(nids) + ")) t GROUP BY nid")
    ret = cur.fetchall()
    for item in ret:
        t_nids.append(item[0])
        word_group.append(item[1].split(','))
        letter_group.append(list(set(list(item[1].replace(',', '')))))  # 用set实现去重
    if len(t_nids) < len(nids):
        lost = list(set(nids).difference(set(t_nids)))
        print '以下', len(lost), '本小说编号未录入数据库：', lost
    return t_nids, word_group, letter_group


def save_similar(con, cur, table, vals, save_limit=None):
    if save_limit is not None:
        vals = sorted(vals, key=lambda x: x[5], reverse=True)[:save_limit]
    cur.executemany(
        "INSERT INTO `" + table + "` (`nid1`, `nid2`, `type`, `word`, `letter`, `total`) VALUES (%s, %s, %s, %s, %s, %s)", vals)
    con.commit()


def tag_vsm(analysis_nids=[], tag_table='', out_table='', target_nids=None, debug=False, save_limit=None):
    con = connect_db()
    cur = con.cursor()
    time_start = time()
    analysis_nids, analysis_word_group, analysis_letter_group = import_tag_data(cur, tag_table, analysis_nids)
    if target_nids is None: # 若target为None，则默认为全量分析
        target_nids, target_word_group, target_letter_group = (analysis_nids, analysis_word_group, analysis_letter_group)
    else:
        target_nids, target_word_group, target_letter_group = import_tag_data(cur, tag_table, target_nids)
    print '导入数据耗时：', time() - time_start
    time_start = time()
    for i in range(0, len(target_nids)):
        vals = []
        for j in range(i+1, len(analysis_nids)):
            letter_similar = vsm(target_letter_group[i], analysis_letter_group[j], debug=debug)
            word_similar = vsm(target_word_group[i], analysis_word_group[j], debug=debug)
            total_similar = (word_similar + letter_similar) / 2
            vals.append((target_nids[i], analysis_nids[j], 'vsm', word_similar, letter_similar, total_similar))
            if debug:
                print 'target', dumps(target_word_group[i],ensure_ascii=False)
                print 'analysis', dumps(analysis_word_group[j],ensure_ascii=False)
                print 'letter_similar:', letter_similar
                print 'word_similar:', word_similar
                print 'total_similar:', total_similar
                print '-----'
        save_similar(con, cur, out_table, vals, save_limit)
    print '分析结束，耗时：', time() - time_start
    cur.close()
    con.close()


if __name__ == '__main__':

    # nids = ['100000092', '100000740']

    con = connect_db()
    cur = con.cursor()
    # cur.execute("SELECT nid FROM `fan_shelf` ORDER BY collect DESC Limit 5")
    cur.execute("SELECT `nid` FROM `novel_info` AS a LEFT JOIN (SELECT DISTINCT `nid1` as `nnid` FROM `similar_base_tag`) AS b ON a.nid = b.nnid WHERE b.nnid IS NULL")
    ret = cur.fetchall()
    analysis_nids = [str(nid[0]) for nid in ret]
    cur.close()
    con.close()

    target_nids = ['100089917', '100055607', '100089784', '100060280',
                   '100087736', '100077651', '100025807', '100084396',
                   '100000514', '100079016', '100072902', '100070345',
                   '100003883', '100057499', '100028599', '100000748',
                   '100061867', '100061338', '100056917', '100011818',
                   '100049348', '100056938', '100035330', '100045203',
                   '100042006']

    debug = False
    tag_vsm(analysis_nids, target_nids=target_nids, tag_table='novel_base_tag', out_table='similar_base_tag', debug=debug)
    tag_vsm(analysis_nids, target_nids=target_nids, tag_table='novel_description_tag', out_table='similar_description_tag', debug=debug)
