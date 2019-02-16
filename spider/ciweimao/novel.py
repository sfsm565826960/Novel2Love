#encoding=utf-8
############
# 抓取所有有效的小说
############
import urllib
import thread
from pyquery import PyQuery as pq
from config import connect_db
from time import sleep
from random import randint


def str2int(str):
    str = str.replace(',', '')
    if str.find('.') >= 0:
        return int(float(str[:-1]) * 10000)
    else:
        return int(str)


def save(pid, nid, name, aid, description, click, collect, length, tags, uids):
    try:
        con = connect_db()
        cursor = con.cursor()
        cursor.execute("INSERT INTO novel_info (`nid`,`name`,`aid`,`description`,`click`,`collect`,`length`) VALUES (%s, %s, %s, %s, %s, %s, %s);", (nid, name, aid, description, click, collect, length))
        tval = []
        for tag in tags:
            tval.append((nid, tag))
        cursor.executemany("INSERT INTO novel_base_tag (`nid`, `tag`) VALUES(%s, %s)", tval)
        uval = []
        for uid in uids:
            uval.append((nid, uid))
        cursor.executemany("INSERT INTO novel_fans (`nid`,`uid`) VALUES(%s, %s)", uval)
        con.commit()
        cursor.close()
        con.close()
        print pid, nid, name, 'SAVE'
    except Exception as e:
        print pid, nid, name, 'Fail:' + str(e)


def novel(nid, novel_length_limit=100000):
    url = 'https://www.ciweimao.com/book/'
    res = urllib.urlopen(url + str(nid))
    dom = pq(res.read())
    title = dom('head>title').text()
    if title == u'刺猬猫':
        raise Exception('INVALID_NOVEL_ID')
    else:
        node = dom('body .book-info .title').contents()
        if node.length < 2:
            raise Exception('IP_LOCK')
        name = node[0].encode('utf-8')
        aid = node[1][0].get('href')
        aid = aid[aid.rfind('/') + 1:]
        tags = dom('head>meta[name=keywords]').attr('content').split(',')
        node = dom('body .breadcrumb').children()
        for tag in node[1:]:
            tags.append(tag.text)
        description = dom('head>meta[name=description]').attr('content')
        node = dom('body .book-grade').children()
        click = str2int(node[0].text)
        collect = str2int(node[1].text)
        length = str2int(node[2].text)
        if length < novel_length_limit:
            raise Exception('INVALID_NOVEL_LENGTH', length)
        res = urllib.urlopen('https://www.ciweimao.com/book/get_book_fans_list?book_id=' + str(nid))
        dom = pq(res.read())
        node = dom('.nickname')
        uids = []
        for user in node:
            user = user.get('href')
            user = user[user.rfind('/') + 1:]
            uids.append(int(user))
        return nid, name, aid, description, click, collect, length, tags, uids


def process(start, end, pid=None):
    con = None
    cur = None
    if pid is not None:
        con = connect_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM `process` WHERE `pid` = " + str(pid))
        ret = cur.fetchall()
        if len(ret) > 0:
            start = ret[0][3]
            end = ret[0][2]
        else:
            cur.execute("INSERT INTO `process` (`pid`, `start`, `end`, `pos`) VALUES (%s, %s, %s, %s)",(pid, start, end, start))
            con.commit()
    for nid in range(start, end):
        try:
            save(pid, *novel(nid))
            if pid is not None:
                cur.execute("UPDATE `process` SET `pos` = %s WHERE `pid` = %s", (nid, pid))
                con.commit()
        except Exception as e:
            if e.message in {'INVALID_NOVEL_ID', 'INVALID_NOVEL_LENGTH'}:
                continue
            elif e.message == 'IP_LOCK':
                print pid, 'IP Lock, Sleep ....', nid
                cur.close()
                con.close()
                sleep(randint(30, 60))
                print pid, 'IP Unlock, ReTry !', nid
                return process(nid, end, pid)
    if pid is not None:
        cur.execute("DELETE FROM `process` WHERE `pid` = " + str(pid))
        con.commit()
        cur.close()
        con.close()
    print pid, 'Finish', start, end


if __name__ == '__main__':
    try:
        nids = ['100059419','100061833','100069085','100076717','100083234','100087710','100087712']
        for nid in nids:
            save(1, *novel(nid))
        exit(0)



        # id = 10006
        # thread.start_new_thread(process, (id * 10000, id * 10000 + 500, 1))
        # thread.start_new_thread(process, (id * 10000 + 500, id * 10000 + 1000, 2))
        # thread.start_new_thread(process, (id * 10000 + 1000, id * 10000 + 1500, 3))
        # thread.start_new_thread(process, (id * 10000 + 1548, id * 10000 + 2000, 4))
        # thread.start_new_thread(process, (id * 10000 + 2000, id * 10000 + 2500, 5))
        # thread.start_new_thread(process, (id * 10000 + 2500, id * 10000 + 3000, 6))
        # thread.start_new_thread(process, (id * 10000 + 3000, id * 10000 + 3500, 7))
        # thread.start_new_thread(process, (id * 10000 + 3500, id * 10000 + 4000, 8))
        # thread.start_new_thread(process, (id * 10000 + 4000, id * 10000 + 4500, 9))
        # thread.start_new_thread(process, (id * 10000 + 4500, id * 10000 + 5000, 10))
        # thread.start_new_thread(process, (id * 10000 + 5000, id * 10000 + 5500, 11))
        # thread.start_new_thread(process, (id * 10000 + 5500, id * 10000 + 6000, 12))
        # thread.start_new_thread(process, (id * 10000 + 6000, id * 10000 + 6500, 13))
        # thread.start_new_thread(process, (id * 10000 + 6500, id * 10000 + 7000, 14))
        # thread.start_new_thread(process, (id * 10000 + 7000, id * 10000 + 7500, 15))
        # thread.start_new_thread(process, (id * 10000 + 7500, id * 10000 + 8000, 16))
        # thread.start_new_thread(process, (id * 10000 + 8000, id * 10000 + 8500, 17))
        # thread.start_new_thread(process, (id * 10000 + 8500, id * 10000 + 9000, 18))
        # thread.start_new_thread(process, (id * 10000 + 9000, id * 10000 + 9500, 19))
        # thread.start_new_thread(process, (id * 10000 + 9500, (id + 1) * 10000, 20))
        # thread.start_new_thread(process, (100060000, 100061000, 0))
        thread.start_new_thread(process, (100050000, 100060000, 1))
        thread.start_new_thread(process, (100040000, 100050000, 2))
        thread.start_new_thread(process, (100030000, 100040000, 3))
        thread.start_new_thread(process, (100020000, 100030000, 4))
        thread.start_new_thread(process, (100010000, 100020000, 5))
        # thread.start_new_thread(process, (100000000, 100010000, 6))
    except Exception as e:
        print str(e)


    con = connect_db()
    cur = con.cursor()
    while 1:
        sleep(30)
        cur.execute("SELECT count(*) FROM `process`")
        ret = cur.fetchall()
        if ret[0][0] > 0:
            pcount = ret[0][0]
            cur.execute("SELECT SUM(pos - start)/SUM(end - start)*100 FROM `process`")
            ret = cur.fetchall()
            print '=====还剩下 ' + str(pcount) + ' 个进程正在运行，总体进度：' + str(ret[0][0]) + ' ====='
        else:
            print '===== 全部结束 ====='
            cur.close()
            con.close()
            exit(0)

