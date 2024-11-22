# -*- coding: utf-8 -*-
# https://files.cnblogs.com/files/zhanghongfeng/file_download.rar

# import scrapy
#
# class HttpbinSpider(scrapy.Spider):
#     name = 'httpbin'
#     allowed_domains = ['httpbin.org']
#     start_urls = ['http://httpbin.org/get']
#
#     def parse(self, response):
#         self.logger.debug(response.text)
#         self.logger.debug('Status Code: ' + str(response.status))

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

# from urlparse import urlparse
# from urlparse import urlunparse

from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib import parse

class TttpSpider(Spider):
    name = 'tttp'
    allowed_domains = ['ivsky.com']
    start_urls = ['https://www.ivsky.com/tupian/ziranfengguang/index_1.html']

    def parse(self, response):
        li_list = response.xpath('//ul[@class="ali"]/li')
        for li in li_list:
            item = FileDownloadItem()
            href = li.xpath('.//img/@src').extract()
            item['href'] = parse.urljoin(base=response.url,url=href[0] if href else None)
            item['image_urls'] = [parse.urljoin(base=response.url,url=href[0] if href else None)]
            yield item

class fileSpider(Spider):
    name="file_download"
    # allowed_domains=['matplotlib.org']
    allowed_domains=['cnblogs.com']
    # start_urls=['http://matplotlib.org/examples/index.html']
    start_urls=['https://www.cnblogs.com/aiyablog/articles/17948703']
    def parse(self,response):
        # le=LinkExtractor(restrict_xpaths='//*[@id="matplotlib-examples"]/div',deny='/index.html$')
        # for link in le.extract_links(response):
        #     print("link.url:", link.url)
        #     yield Request(link.url, callback=self.parse_link)

        file = FileDownloadItem()
        # file['file_urls']=[href]
        file['file_urls'] = [
            "https://storage.googleapis.com/chrome-for-testing-public/133.0.6843.0/win64/chromedriver-win64.zip"]
        return file

        # loader = ItemLoader(item=FileDownloadItem())
        # loader.add_value('file_urls', "https://storage.googleapis.com/chrome-for-testing-public/133.0.6843.0/win64/chromedriver-win64.zip")
        # yield loader.load_item()
    def parse_link(self,response):
        # pattern=re.compile('href=(.*\.py)')
        pattern=re.compile('')
        div=response.xpath('/html/body/div[4]/div[1]/div/div')
        p=div.xpath('//p')[0].extract()
        link=re.findall(pattern,p)[0]
        if ('/') in link:
            href='http://matplotlib.org/'+link.split('/')[2]+'/'+link.split('/')[3]+'/'+link.split('/')[4]
        else:
            link=link.replace('"','')
            scheme=urlparse(response.url).scheme
            netloc=urlparse(response.url).netloc
            temp=urlparse(response.url).path
            path='/'+temp.split('/')[1]+'/'+temp.split('/')[2]+'/'+link
            combine=(scheme,netloc,path,'','','')
            href=urlunparse(combine)
#            print href,os.path.splitext(href)[1]
        file=FileDownloadItem()
        # file['file_urls']=[href]
        file['file_urls']=["https://storage.googleapis.com/chrome-for-testing-public/133.0.6843.0/win64/chromedriver-win64.zip"]
        print("file_urls href:", href)
        return file

class TestSeleniumSpider(Spider):
    name = 'testSele'
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

class TestImgSpider(Spider):
    name = 'img'
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