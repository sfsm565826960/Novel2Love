#encoding=utf-8
################
# 利用百度翻译实现代理
################
from urllib import quote, unquote, urlopen
from re import compile, sub, findall


def proxy_baidu_fanyi(url, data=None):
    if data is not None:
        raise Exception('Proxy_Baidu_Fanyi Unsupport data')
    url_fanyi = 'http://translate.baiducontent.com/transpage?from=yue&to=zh&source=url&frzj=cfy&query='
    query = quote(url, safe='')
    res = urlopen(url_fanyi + query)
    html = res.read()
    html = html[277:html.rfind('<!--"\'>-->')]  # 去掉前后fanyi的脚本
    # 移除错误脚本
    html = sub(compile("<script.{31}createElement.{2}trans.+?>"), '', html)
    # 移除trans标签
    html = html.replace('</trans>', '')
    html = sub(compile('<trans.+?>'), '', html)
    # 修正 < 和 > ，用于提取字数\收藏\点击
    html = html.replace('&#60;', '<')
    html = html.replace('&#62;', '>')
    # 修正URL链接
    hrefs = findall(compile('(https://trans.+?query=(.+?)&.+?)[\'"]'), html)
    for href in hrefs:
        html = html.replace(href[0], unquote(href[1]))
    return html


if __name__ == '__main__':
    proxy_baidu_fanyi('https://www.ciweimao.com/book/get_book_fans_list?book_id=100059419')
