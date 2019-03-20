import json
import requests
import re
from scrapy.selector import Selector
#

def make_unicode(value, prefer_encodings=None):
    if prefer_encodings is None:
        prefer_encodings = ['utf8', 'gbk', 'gbk?']
    if isinstance(value, str) or value is None:
        return value
    if not isinstance(value, str):
        return value
    for enc in prefer_encodings:
        try:
            if enc.endswith('!'):
                return value.decode(enc[:-1], 'ignore')
            elif enc.endswith('?'):
                return value.decode(enc[:-1], 'replace')
            elif enc.endswith('&'):
                return value.decode(enc[:-1], 'xmlcharrefreplace')
            elif enc.endswith('\\'):
                return value.decode(enc[:-1], 'backslashreplace')
            else:
                return value.decode(enc)
        except UnicodeError:
            pass
    else:
        raise


def get_down_urls(url):
    response = requests.get(url, verify=False)
    response = Selector(text=make_unicode(response.text))
    alist = response.xpath('.//script')
    for href in alist:
        scripts_content = href.get()
        scripts_content = re.sub(r'[\n\t\r]', '', scripts_content)
        # print scripts_content
        if re.search('window.__init__', scripts_content):
            start_pos = scripts_content.index("{")
            end_pos = scripts_content.rindex("}")
            # print scripts_content[start_pos:end_pos + 1]
            json_str = json.loads(scripts_content[start_pos:end_pos + 1])
            cid = json_str['list'][0]['cid']
            title = json_str['title']
            print
            title
            aid = json_str['aid']
            print
            aid

            donwlaod_url = "https://www.kanbilibili.com/api/video/%s/download?cid=%s&quality=112&page=1" % (aid, cid)
            get_download_urls = requests.get(donwlaod_url)
            get_download_urls = json.loads(get_download_urls.text)
            durls = get_download_urls['data']['durl']
            for durl in durls:
                down_url = durl['url']
                down_order = durl['order']
                print
                "down load url : %s " % down_url


def Get_spalce_AVList(url):
    re_mid = re.search(r'\/([\d]+)\/', url)
    if re_mid:
        mid = re_mid.group(1)
    else:
        print
        "url error can find mid in url"
        return
    aidList = []
    page = 1
    while True:
        url_vlist = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid=%s&pagesize=100&tid=0&page=%s&keyword=&order=pubdate" % (
        mid, page)
        # print url_vlist
        response = requests.get(url_vlist, verify=False)
        vlist = json.loads(response.text)
        for info in vlist['data']['vlist']:
            aidList.append(info['aid'])
            # print info['aid']
        if vlist['data']['pages'] > page:
            page = page + 1
        else:
            break
    for aid in aidList:
        url_downLoad = "https://www.kanbilibili.com/video/av%s" % aid
        print
        url_downLoad
        get_down_urls(url_downLoad)


if __name__ == "__main__":
    space_url = "https://space.bilibili.com/97678687/#/video?tid=0&page=1&keyword=&order=pubdate"
    Get_spalce_AVList(space_url)
