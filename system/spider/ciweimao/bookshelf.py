#encoding=utf-8
############
# 抓取用户的书架数据
############
import urllib
import thread
from pyquery import PyQuery as pq
from config import connect_db
from time import sleep
from random import randint


def get_user_shelf(uid):
    url = 'https://www.ciweimao.com/bookshelf/'
    res = urllib.urlopen(url + str(uid))
    dom = pq(res.read())
    title = dom('head>title').text()
    if title != u'刺猬猫':
        shelf = []
        node = dom('body .book-list li>div>a')
        if len(node) == 0:
            if title == u'欢乐书客':
                # print uid, IP LOCK
                return []
            else:
                print uid, title, "SAVE, BookCount: 0"
                return [(uid, 0)]  # 该用户无书籍,用0来标识该用户已获取
        for a in node:
            nid = a.get('href')
            nid = nid[nid.rfind('/') + 1:]
            shelf.append((uid, nid))
        print uid, title, "SAVE, BookCount:", len(shelf)
        return shelf


def process(start, end, pid=None):
    url = 'https://www.ciweimao.com/bookshelf/'
    con = connect_db()
    cur = con.cursor()
    if pid is not None:
        cur.execute("SELECT * FROM `process` WHERE `pid` = " + str(pid))
        ret = cur.fetchall()
        if len(ret) > 0:
            start = ret[0][3]
            end = ret[0][2]
        else:
            cur.execute("INSERT INTO `process` (`pid`, `start`, `end`, `pos`) VALUES (%s, %s, %s, %s)", (pid, start, end, start))
            con.commit()
    cur.execute("SELECT DISTINCT `uid` FROM `novel_fans` WHERE `uid` BETWEEN %s AND %s ORDER BY uid", (start, end))
    ret = cur.fetchall()
    for uid in ret:
        uid = uid[0]
        shelf = get_user_shelf(uid)
        if len(shelf) == 0:
            print pid, "IP LOCK, Sleep ...", uid
            sleep(randint(60, 120))
            print pid, "IP Unlock, ReTry !", uid
            cur.close()
            con.close()
            return process(uid, end, pid)
        else:
            cur.executemany("INSERT INTO `fan_shelf` (`uid`, `nid`) VALUES (%s, %s)", shelf)
            cur.execute("UPDATE `process` SET `pos` = %s WHERE `pid` = %s", (uid, pid))
            con.commit()
            sleep(randint(2, 5))
    if pid is not None:
        cur.execute("DELETE FROM `process` WHERE `pid` = " + str(pid))
        con.commit()
        cur.close()
        con.close()
    print pid, 'Finish', start, end


get_user_shelf(1248035)
exit(0)
process_id = 3000
con = connect_db()
cur = con.cursor()
cur.execute("SELECT DISTINCT `uid` FROM `novel_fans` AS a LEFT JOIN (SELECT DISTINCT `uid` as `uuid` FROM `fan_shelf`) AS b ON a.uid = b.uuid WHERE b.uuid IS NULL ORDER BY a.uid")
ret = cur.fetchall()
group = ret[::10000]
group.append(ret[-1:][0])
try:
    for i in range(0, len(group)-1):
        thread.start_new_thread(process, (group[i][0], group[i+1][0], process_id + i))
except Exception as e:
    print str(e)

while 1:
    sleep(30)
    cur.execute("SELECT count(*) FROM `process` WHERE ROUND(pid/"+str(process_id)+")=1")
    ret = cur.fetchall()
    if ret[0][0] > 0:
        pcount = ret[0][0]
        cur.execute("SELECT SUM(pos - start)/SUM(end - start)*100 FROM `process` WHERE ROUND(pid/"+str(process_id)+")=1")
        ret = cur.fetchall()
        print '=====还剩下 ' + str(pcount) + ' 个进程正在运行，总体进度：' + str(ret[0][0]) + ' ====='
    else:
        print '===== 全部结束 ====='
        cur.close()
        con.close()
        exit(0)

