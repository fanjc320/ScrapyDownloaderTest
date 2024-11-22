# -*- coding: utf-8 -*-
import scrapy
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
from selenium.webdriver.common.by import By
class ApkPureSpider(Spider):
    name = 'apkpure'
    allowed_domains = ['apkpure.com']
    start_urls = ['https://apkpure.com/game_casual']

    def __init__(self):
        super().__init__()
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        # self.url = 'https://xxxx/xxx/xxx/'
        self.proxies = {
            "http": "http://127.0.0.1:10819",
            "https": "http://127.0.0.1:10819",
        }
        self.browser = webdriver.Chrome()

        # self.browser.get(r'https://www.baidu.com/')
        # # 设置分辨率 500*500
        # self.browser.set_window_size(500, 500)
        # time.sleep(5)
        # self.browser.quit()

    def start_requests(self):
        # yield scrapy.Request(
        #     url="https://apkpure.com/game_casual",
        #     headers=self.headers,
        #     callback=self.parse,
        #     dont_filter=True
        # )

        self.browser.get(r'https://apkpure.com/game_casual')

        # latestGames = self.browser.find_elements(By.XPATH, '//main/div[5]/div[2]/div[1]/div/div/ul/li[@class="grid-col"]//div[@class="grid-row"]')
        latestGames = self.browser.find_elements(By.XPATH, '//main/div[5]/div[2]/div[1]/div/div/ul/li/div/a[contains(@class, "apk-grid-button")]')
        print("latestGame:", latestGames)
        count = 1
        for i in range(len(latestGames)):
            if count > 2:
                break
            # latestGames[i].find_element(By.XPATH, '@[class=]')
            self.browser.implicitly_wait(5)
            item = latestGames[i]
            print(f'item:{i}:\t{item}')
            item.screenshot("item.png")
            ActionChains(self.browser).move_to_element(item).perform()
            # latestGames[i].click()
            ++count
            # item = self.browser.find_elements_by_xpath('//*[@id="duya-header"]/div/div/div[1]/div[i+1]')
        # index = latestGame.xpath('').get()
        # print("index:", index)
        # for index in latestGame: latestGame is not iterable
        #     index.click()
        # oldVersionBtn = self.browser.find_element(By.XPATH, '//main//a[@title="Old Versions"]')
        # oldVersionBtn.click()

    # 时间长就不给爬了好像
    def parse(self, response):
        # print(response.body) # 好像改成动态加载了，所以下面获取不到，
        print("response.text:", response.text) # 访问频繁!
        # return
        li_list = response.xpath('//div/div//li[@class="grid-col"]')
        # li_list = response.xpath('//ul[@class="ali"]')
        print("len(li_list):", len(li_list))
        print("li_list:", li_list)
        count = 1
        for li in li_list:
            if count > 2:
                break
            # # print("li:::", li)
            # item = ImgDownloadItem()
            oldVersionUrl = li.xpath('./div/a[contains(@class,"apk-grid-download")]/@href').extract_first()
            print("apkpure oldVersionUrl:", oldVersionUrl)
            self.openOldVersionUrl(oldVersionUrl)
            count += 1
            # yield response

            # yield scrapy.Request(href, callback=self.downloadUrl)

    def downloadUrl(self, response):
        versionsUrl = response.xpath('//a[@title="Old Versions"]/@href').extract_first()
        if not versionsUrl:
            print("downloadUrl versionsUrl error")
        print("downloadUrl versionsUrl:", versionsUrl)
        yield scrapy.Request(versionsUrl, callback=self.downloadUrl)

    def openOldVersionUrl(self,url):
        self.browser.get(url)
        # self.browser.get(r'https://www.baidu.com/')
        # 设置分辨率 500*500
        self.browser.set_window_size(1000, 1500)
        oldVersionBtn = self.browser.find_element(By.XPATH, '//main//a[@title="Old Versions"]')
        # oldVersionBtn = self.browser.find_element_by_xpath('//main//a[@title="Old Versions"]')
        oldVersionBtn.click()
        print("oldVersionBtn:", oldVersionBtn)

        moreVersionBtn = self.browser.find_element(By.XPATH, '//a[@class="more-version"]')
        moreVersionBtn.click()
        # time.sleep(2)
        # self.browser.quit()

        # scrapy.Request()
