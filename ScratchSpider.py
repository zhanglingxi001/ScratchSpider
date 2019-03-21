#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree
import requests
import re
import os
import json
import zipfile

class ScratchSpider:

    def __init__(self, rangeNum):
        self.rangeNum = rangeNum
        self.headers = {"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36"}
        self.start_url = "https://scratch.mit.edu/projects/{}/remixes/"
        self.download_url = "https://projects.scratch.mit.edu/{}"
        self.file_path = "./sb3Files/{}_remixing"
        self.id = []

    def StartDownload(self):
        url = "https://api.scratch.mit.edu/explore/projects?limit=16&offset={}&language=en&mode=popular&q=*"
        for x in range(0, self.rangeNum):
            url_1 = url.format(str(x * 16))
            print(url_1)
            response = requests.get(url_1, headers=self.headers)
            string = response.json()
            for y in range(0, 16):
                self.id.append(str(string[y]["id"]))
                print(str(string[y]["id"]))

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_id(self, html_str):
        html = etree.HTML(html_str)
        result = html.xpath('//span[@class="title"]/a/@href')
        id_lists = [re.findall("/projects/(.*?)/", i)[0] for i in result]
        return id_lists

    def download(self, id_lists, id):
        folder = os.path.exists(self.file_path.format(id))
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(self.file_path.format(id))
        for i in id_lists:
            try:
                print(i)
                response = requests.get(self.download_url.format(i), headers=self.headers)
                project = response.json()
                print('load json data success')
                print('generate ZIP...')
                zipfile_name = i + '.sb3'
                print(zipfile_name)
                sb3 = zipfile.ZipFile(self.file_path.format(id)+"/"+zipfile_name, 'w')
                sb3.writestr('project.json', json.dumps(project).encode())
                sb3.close()
                print('generate ZIP OK !')
            except Exception as e:
                print(repr(e))
        print("------------------------------------")

    def run(self):
        self.StartDownload()
        for i in self.id:
            print(i)
            html_str = self.parse_url(self.start_url.format(i))
            id_lists = [i]+self.get_id(html_str)
            print(id_lists)
            self.download(id_lists, i)


if __name__ == '__main__':
    spider = ScratchSpider(10)
    spider.run()


