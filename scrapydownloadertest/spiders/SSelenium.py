# -*- coding: utf-8 -*-

from scrapy.spiders import Spider,CrawlSpider,Rule
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import FormRequest
from scrapydownloadertest.items import FileDownloadItem, ImgDownloadItem
from scrapy.utils.response import open_in_browser
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import sys
import re
import os

from urllib import parse

from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains


# browser = webdriver.Chrome()
# browser.get(r'https://www.baidu.com/')
# # 设置分辨率 500*500
# browser.set_window_size(500,500)
class TestSeleSpider(Spider):
    name = 'sele'
    # allowed_domains = ['ivsky.com']
    # start_urls = ['https://www.ivsky.com/tupian/ziranfengguang/index_1.html'] # 好像改成动态加载了，所以下面获取不到
    allowed_domains = ['51miz.com']
    start_urls = ['https://www.51miz.com/sucai/?utm_term=24405007&utm_source=bing&msclkid=b3884ee7273e10112f6329da63812449']

    # 时间长就不给爬了好像
    def parse(self, response):
        # print(response.body) # 好像改成动态加载了，所以下面获取不到，
        print(response.text) # 访问频繁!
        return
        li_list = response.xpath('//div[@class="recommend-preview miz-image-box"]')
        # li_list = response.xpath('//ul[@class="ali"]')
        print("len(li_list):", len(li_list))
        print("li_list:", li_list)
        for li in li_list:
            print("li:::", li)
            item = ImgDownloadItem()
            href = li.xpath('.//img/@src').extract()
            item['href'] = parse.urljoin(base=response.url,url=href[0] if href else None)
            item['image_urls'] = [parse.urljoin(base=response.url,url=href[0] if href else None)]
            print("sele href:", href)
            print("sele item image_urls:", item['image_urls'])
            yield item