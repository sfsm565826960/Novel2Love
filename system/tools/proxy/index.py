#coding=utf-8
###############
# 默认HTTP请求，可支持加载代理函数
###############
import urllib


def urlopen(url, data=None, proxy=None):
    if proxy is None:
        return urllib.urlopen(url, data).read()
    elif hasattr(proxy, '__call__'):
        return proxy(url, data)