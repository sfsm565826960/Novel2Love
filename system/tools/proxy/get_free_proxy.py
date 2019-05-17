#encoding=utf-8
#############
# 获取免费代理
#############
import urllib
from random import randint
from pyquery import PyQuery as pq


def kuaidaili(page=None):
    if page is None:
        page = randint(1, 10)
    url = 'https://www.kuaidaili.com/free/inha/' + str(page)
    res = urllib.urlopen(url)
    dom = pq(res.read())
    node = dom('#list tr')
    list = []
    for item in node[1:]:
        if item[3].text.upper() == 'HTTP':
            list.append({ "http": item[0].text + ":" + item[1].text })
        elif item[3].text.upper() == 'HTTPS':
            list.append({"https": item[0].text + ":" + item[1].text})
    return list


def feiyi(page=None):
    url = 'http://www.feiyiproxy.com/?page_id=1457'
    res = urllib.urlopen(url)
    dom = pq(res.read())
    node = dom('.et_pb_code table tr')
    list = []
    for item in node[1:]:
        if item[3].text.upper() == 'HTTP':
            list.append({"http": item[0].text + ":" + item[1].text})
        elif item[3].text.upper() == 'HTTPS':
            list.append({"https": item[0].text + ":" + item[1].text})
    return list


if __name__ == '__main__':
    print 'kuaidaili', kuaidaili()
    print 'feiyi', feiyi()
