#encoding=utf-8
###############
# 修复无作者ID的数据
###############
import urllib
from pyquery import PyQuery as pq
from config import connect_db
from time import sleep
from random import randint


def process():
    url = 'https://www.ciweimao.com/book/'
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT `nid` FROM `novel_info` WHERE `aid` = 0")
    ret = cur.fetchall()
    count = len(ret)
    index = 0
    for nid in ret:
        nid = nid[0]
        res = urllib.urlopen(url + str(nid))
        dom = pq(res.read())
        node = dom('body .book-info .title').contents()
        if node.length < 2:
            print 'IP Lock, Sleep ....', nid
            cur.close()
            con.close()
            sleep(randint(30, 60))
            print 'IP Unlock, ReTry !', nid
            return process()
        name = node[0].encode('utf-8')
        aid = node[1][0].get('href')
        aid = aid[aid.rfind('/') + 1:]
        cur.execute("UPDATE `novel_info` SET `aid` = %s WHERE `nid` = %s", (aid, nid))
        con.commit()
        index = index + 1
        print nid, aid, "(" + str(index) + "/" + str(count) + ")"
    cur.close()
    con.close()


process()