# -*- coding:utf-8 -*-

"""
@author: Yan Liu
@file: crawl.py
@time: 2018/3/27 11:43
@desc: 爬取百度图片
"""

import requests
import threading
import os


def getPages(keyword, pages):
    params = []
    for i in range(30, 30 * pages + 30, 30):
        params.append({
            'tn': 'resultjson_com',
            'ipn': 'rj',
            'ct': 201326592,
            'is': '',
            'fp': 'result',
            'queryWord': keyword,
            'cl': 2,
            'lm': -1,
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': '',
            'z': '',
            'ic': '',
            'word': keyword,
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': '',
            'istype': '',
            'qc': '',
            'nc': 1,
            'fr': '',
            'pn': i,
            'rn': 30,
            'gsm': '1e',
            '1488942260214': ''
        })

    url = 'https://image.baidu.com/search/acjson'
    urls = []
    fail_url_count = 0
    for i in params:
        response = requests.get(url, params=i)
        try:
            jsonObj = response.json()
            urls.append(jsonObj.get('data'))
        except Exception as e:
            print("json数据格式错误 " + str(e))
            fail_url_count += 1
    print("提取图片url成功：%d 失败：%d" % (len(urls), fail_url_count))
    return urls


x = 0


def getImg(keyword, dataList, localPath):
    global x
    if not os.path.exists(localPath):
        os.mkdir(localPath)

    for list in dataList:
        for i in list:
            if i.get('hoverURL') != None:
                try:
                    print('正在下载：%s' % i.get('hoverURL'))
                    ir = requests.get(i.get('hoverURL'))
                    open(localPath + ('%s-%d.jpg' % (keyword, x)), 'wb').write(ir.content)
                    x += 1
                except Exception as e:
                    print("图片下载失败" + i.get('hoverURL') + str(e))

    print('%s图片下载完成' % keyword)


def get_img(keyword_list, page_num, img_dir):
    for name in keyword_list:
        dataList = getPages(name, page_num)
        getImg(name, dataList, img_dir)


if __name__ == '__main__':

    flower_list = ['玫瑰', '兰花']

    dog_list = ['哈士奇', '吉娃娃']

    cat_list = ['折耳', '英短']

    get_img(flower_list, 500, './flower/')
    # get_img(dog_list, 500, './dog/')
    # get_img(cat_list, 100, './cat/')

    '''
    # 并行抓取
    threads = []

    t1 = threading.Thread(target=get_img, args=(flower_list, 500, './flower/'))
    threads.append(t1)

    t2 = threading.Thread(target=get_img, args=(dog_list, 500, './dog/'))
    threads.append(t2)

    t3 = threading.Thread(target=get_img, args=(cat_list, 100, './cat/'))
    threads.append(t3)

    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()
    '''

    print("一共下载%d张图片" % x)
