#encoding=utf-8
import urllib
import json
import sys
from config import connect_db
reload(sys)
sys.setdefaultencoding('utf-8')

def getKeyWord(str):
    try:
        res = urllib.urlopen('http://ictclas.nlpir.org/nlpir/index5/getKeyWords.do', data=urllib.urlencode({"content": str}))
        j = json.loads(res.read())
        keywords = j["keywords"].split('#')
        return keywords[:-1]
    except Exception as e:
        print e
        return []


if __name__ == '__main__':
    con = connect_db()
    cur =  con.cursor()
    cur.execute("SELECT `nid`, `description` FROM `novel_info` as a LEFT JOIN (SELECT DISTINCT `nid` as `nnid` FROM `novel_description_tag`) as b ON a.nid = b.nnid WHERE b.nnid IS NULL")
    ret = cur.fetchall()
    for row in ret:
        keywords = getKeyWord(row[1])
        kval = []
        for k in keywords:
            kval.append((row[0], k))
            print row[0], k
        if len(kval) > 0:
            cur.executemany("INSERT INTO `novel_description_tag` (`nid`, `tag`) VALUES (%s, %s)", kval)
            con.commit()
            print '-----'
    cur.close()
    con.close()