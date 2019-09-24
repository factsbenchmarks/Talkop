'''
http://bbs.talkop.com/
抓取海贼王论坛

收获（都很牛逼）
    1 发现用类写爬虫 比用函数写爬虫爽一些，有些参数不用一直传，都在__init__中，在这里就是self.data_list。
    2 json 终于意识到json的价值了，把列表类型转换成json类型，保存在文件中，可以从文件中copy出来，有转化json类型的网站，直接转化下，就可以看到其中的数据了
    3 etree的使用，参数是bytes类型
'''

import requests
import json
from lxml import etree


class TalkopSpider(object):
    def __init__(self):
        self.url = 'http://bbs.talkop.com/forum-fenxi-{}.html'
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            }
        self.data_list = []

    def get_response(self,url):
        '''
        发请求，获取网页内容
        :param url:
        :return:
        '''
        response = requests.get(url=url,headers=self.headers)
        return response.content

    def parse_data(self,data):
        '''
        接收bytes类型页面值，解析之，获取需要提取的数据，
        :param data:
        :return:
        '''
        # data是bytes类型
        # 转类型
        x_data = etree.HTML(data)
        titles = x_data.xpath("//a[@class='s xst']/text()")
        urls = x_data.xpath("//a[@class='s xst']/@href")
        # 用这种方法，实现title，url一一对应。
        for index,title in enumerate(titles):
            news = {}
            news[title] = urls[index]
            self.data_list.append(news)


    def save_data(self):
        '''
        将列表类型转换为json类型
        :param data:
        :return:
        '''
        j_data = json.dumps(self.data_list)
        with open('day6.json','w') as f:
            f.write(j_data)

    def run(self):
        for i in range(1,10):
            url = self.url.format(i)
            data = self.get_response(url)
            self.parse_data(data)
        self.save_data()
TalkopSpider().run()