# -*- coding: utf-8 -*-
import re, time, json
import aiohttp, asyncio

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}


# 访问主页返回html
async def get_index_url(page):
    try:
        if page == 1:
            url = 'http://www.mmjpg.com/'
            print('page == 1')
        else:
            url = 'http://www.mmjpg.com/home/' + str(page)
        #timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        print("index_url status_code == 200")
                        html = await resp.text()
                        print('返回index_url')
                        parse_index_url(html)
            except:
                pass
    except ConnectionError as e:
        print("Error", e.args)

# 解析主页html图片url
def parse_index_url(html):
    print('开始解析index_url')
    urls = re.findall('<li.*?<a.*?href="(.*?)".*?target.*?>.*?</li>', html, re.S)
    a = 'http://www.mmjpg.com'
    for i in urls:
        if i not in a:
            loop1 = asyncio.get_event_loop()
            loop1.run_until_complete(get_Image_url(i))
            

# 访问图片URL搞到html
async def get_Image_url(url):
    #timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession() as session:
        try:
            for i in range(2, 70):
                print("33333333333333333333333333", i)
                urls = url + '/' + str(i)
                async with session.get(urls, headers=headers) as resp:
                    if resp.status == 200:
                        print('Image_html status_code == 200')
                        html = await resp.text()
                        parse_Image_url(html, urls)
        except:
            pass

# 解析图片URL相关信息
def parse_Image_url(html, url):
    print('返回index_url')
    results = re.findall(
        'id="content".*?<a.*?img.*?src="(.*?)" data-img="(.*?)" alt="(.*?)".*?>', html, re.S)
    for r in results:
        result = {
            'url': url,
            'src': r[0],
            'alt': r[2]
        }
        print(result)
        print('开始保存..........')
        save_to_json(result)

# 保存信息到本地JSON
def save_to_json(result):
    if result:
        with open('mmjpg2.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, indent=2, ensure_ascii=False))
            f.close()
            print('保存成功-----')

def main():
    start = time.time()
    page = int(input('请输入要爬取的页数: '))
    for i in range(1, page+1):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_index_url(i))
    end = time.time()
    print('程序共耗时: ', end - start)

if __name__ == '__main__':
    main()