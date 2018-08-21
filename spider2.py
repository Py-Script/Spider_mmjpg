# -*- coding: utf-8 -*-
import requests, re, time, os, json
from hashlib import md5
from requests.exceptions import RequestException

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

# 访问主页返回html
def get_index_url(page):
    try:
        if page == 1:
            url = 'http://www.mmjpg.com/'
            print('page=1')
        else:
            url = 'http://www.mmjpg.com/home/' + str(page)
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            print("index_url status_code == 200")
            h = req.content
            html = h.decode('utf-8')
            print('返回index_url')
            return parse_index_url(html)
    except ConnectionError as e:
        print("Error", e.args)
        return None

# 解析主页html图片url
def parse_index_url(html):
    print('开始解析index_url')
    urls = re.findall('<li.*?<a.*?href="(.*?)".*?target.*?>.*?</li>', html, re.S)
    a = 'http://www.mmjpg.com'
    for i in urls:
        if i not in a:
            print(i)
            Image_html(i)
            


def Image_html(url):
    try:
        for i in range(1, 65):
            urls = url + '/' + str(i)
            print(urls)
            req = requests.get(urls, headers=headers)
            if req.status_code == 200:
                print('Image_html status_code == 200')
                h = req.content
                html = h.decode('utf-8')
                results = re.findall('id="content".*?<a.*?img.*?src="(.*?)" data-img="(.*?)" alt="(.*?)".*?>', html, re.S)
                for r in results:
                    result = {
                        'url': urls,
                        'src': r[0],
                        'data-img': r[1],
                        'alt': r[2]
                    }
                    print(result)
                    print('开始保存')
                    save_to_json(result)
    except:
        pass

def save_to_json(result):
    if result:
        with open('mmjpg.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, indent=2, ensure_ascii=False))
            f.close()
            print('保存成功-----')

if __name__ == '__main__':
    start = time.time()
    page = int(input('请输入要爬取的页数: '))
    for i in range(page):
        get_index_url(i)
    end = time.time()
    print('程序共耗时: ', end - start)