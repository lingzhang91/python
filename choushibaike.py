#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# @Time    : 16-6-5 下午1:48
# @Author  : leon
# @Site    : 
# @File    : qiushibaike.py
# @Software: PyCharm


import urllib.request
import re


class QSBK(object):
    def __init__(self):
        # 定义url
        self.url = 'http://www.qiushibaike.com/hot/page/'
        # 定义user_agent
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 定义headers
        self.headers = {'User-Agent': self.user_agent}
        # 全局段子列表，一个元素是一页段子
        self.stories = []
        # 全局要加载的页数
        self.page_index = 1

    def get_page(self):
        '''获取页面源码'''
        try:
            url = self.url + str(self.page_index)
            request = urllib.request.Request(url, headers=self.headers)
            page_code = urllib.request.urlopen(request).read()
            page_code = page_code.decode('UTF-8')
            return page_code
        except:
            return None

    def page_items(self):
        '''根据源码解析数据'''
        page_code = self.get_page()
        if not page_code:
                print('Page load error!')
                return None
        pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</', re.S)
        items = re.findall(pattern, page_code)
        page_stories = []
        for i in items:
            have_img = re.search("img", i[1])
            if not have_img:
                page_stories.append([i[0].strip(), i[1].strip().replace('<br/>', '\n'), i[2].strip()])
        return page_stories

    def load_page(self):
        '''判断是否需要加载数据，并将数据放入全局段子列表'''
        if len(self.stories) < 2:
            page_stories = self.page_items()
            if page_stories:
                self.stories.append(page_stories)
                self.page_index += 1

    def one_story(self, page_story):
        '''从全局段子列表中的一个元素得到一个段子，并获取用户输入值'''
        for story in page_story:
            inp = input()
            if inp == 'q':
                exit()
            header = "第%s页\t发布人:%s\t赞:%s\n"\
                     % (self.page_index - 1, story[0], story[2])
            body = story[1] + '\n=================================\n'
            print(header, body)

    def start(self):
        print('正在读取，回车查看，q退出')
        while True:
            self.load_page()
            if len(self.stories) > 0:
                # 获取全局段子列表中的第一个元素然后删除，并传入到one_story处理
                page_story = self.stories[0]
                del self.stories[0]
                self.one_story(page_story)

qiu = QSBK()
qiu.start()