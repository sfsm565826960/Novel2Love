#encoding=utf-8
from config import connect_db


def update_process():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT `pid` FROM `process`")
    ret = cur.fetchall()
    for pid in ret:
        pid = pid[0]
        print 'update:', pid
        cur.execute("UPDATE `process` SET `pos` = IFNULL((SELECT c.nid FROM (SELECT nid FROM `novel_info` as a, `process` as b WHERE b.pid = %s and a.nid > b.start and a.nid < b.end ORDER BY nid DESC LIMIT 1) c), 0) WHERE pid = %s", (pid, pid))
    con.commit()
    cur.close()
    con.close()


if __name__ == '__main__':
    update_process()