#encoding=utf-8
##################
# 带随机代理的请求
##################

import urllib2
from random import choice

USER_AGENTS = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
]


def urlopen(url, data=None, proxy=None):
    header = {
        "User-Agent": choice(USER_AGENTS)
    }
    handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(handler)
    req = urllib2.Request(url, data=data, headers=header)
    return opener.open(req, timeout=3)


def check_proxy(proxy_list, url = 'http://www.baidu.com'):
    list = []
    for proxy in proxy_list:
        try:
            res = urlopen(url)
            print proxy, res.code
            if res.code == 200:
                list.append(proxy)
        except Exception as e:
            print proxy, e
    return list



if __name__ == '__main__':
    from get_free_proxy import kuaidaili
    proxy_list = []
    for i in range(1, 10):
        proxy_list = proxy_list + check_proxy(kuaidaili(page=i), url='https://www.ciweimao.com/book/100087736')
    print proxy_list